import os
import json
import sys

sys.path.append("/usr/lib/python3/dist-packages")

import salt.config
import salt.utils.event
from salt.client import LocalClient
from salt.runner import RunnerClient
from salt.wheel import WheelClient

from api.utils import RawCommand
from ..models import Minions, Functions, MinionsCustomFields, Keys, Schedule

master_conf = os.environ.get("SALT_URL", "/etc/salt/master")
opts = salt.config.master_config(master_conf)
local = LocalClient(c_path=master_conf)
runner = RunnerClient(opts)
wheel = WheelClient(opts)


def get_keys(refresh=False):
    if refresh:
        # Salt return to minion status.
        minion_status = {
            "minions_rejected": "rejected",
            "minions_denied": "denied",
            "minions_pre": "unaccepted",
            "minions": "accepted",
        }
        api_ret = wheel.cmd(fun="key.list_all")

        Keys.objects.all().delete()
        for key, value in minion_status.items():
            for minion in api_ret[key]:
                finger_ret = wheel.cmd("key.finger", [minion])
                obj, created = Keys.objects.update_or_create(
                    minion_id=minion,
                    defaults={"status": value, "pub": finger_ret[minion]},
                )

    return Keys.objects.all()


def refresh_minion(minion_id):
    grain = local.cmd(minion_id, "grains.items")
    if grain.get(minion_id):
        pillar = local.cmd(minion_id, "pillar.items")
        Minions.objects.update_or_create(
            minion_id=minion_id,
            defaults={
                "grain": json.dumps(grain[minion_id]),
                "pillar": json.dumps(pillar[minion_id]),
            },
        )
        minion_fields = MinionsCustomFields.objects.values(
            "name", "function"
        ).distinct()
        for field in minion_fields:
            command = RawCommand("salt {} {}".format(minion_id, field["function"]))
            custom_field_return = run_raw(command.parse())
            MinionsCustomFields.objects.update_or_create(
                name=field["name"],
                function=field["function"],
                minion=Minions.objects.get(minion_id=minion_id),
                defaults={"value": json.dumps(custom_field_return[minion_id])},
            )


def run_raw(load):

    client = load[0]["client"]
    del load[0]["client"]

    api_mapping = {
        "local": local.cmd,
        "local_async": local.run_job,
        "runner": runner.cmd,
        "runner_async": runner.low,
        "wheel": wheel.cmd,
        "wheel_async": wheel.low,
    }

    api_func = api_mapping[client]
    if ("runner" in client or "wheel" in client) and ("async" in client):
        fun = load[0]["fun"]
        api_ret = api_func(fun=fun, low=load[0])
    else:
        api_ret = api_func(**load[0])

    return api_ret


def get_events():
    def listen():
        event = salt.utils.event.get_event(
            "master",
            sock_dir=opts["sock_dir"],
            transport=opts["transport"],
            opts=opts,
            listen=True,
        )
        stream = event.iter_events(full=True, auto_reconnect=True)
        yield str("retry: 400\n")
        while True:
            data = next(stream)
            yield str("tag: {0}\n").format(data.get("tag", ""))
            yield str("data: {0}\n\n").format(salt.utils.json.dumps(data))

    return listen()


def init_db(target):
    # Modules.
    modules_func = local.cmd(target, "sys.list_functions")[target]

    modules_doc = local.cmd(target, "sys.doc")[target]

    for func in modules_func:
        desc = modules_doc[func]

        Functions.objects.update_or_create(
            name=func, type="local", description=desc or ""
        )
    # Runner.
    # TODO: Factorize.
    runner_func = local.cmd(target, "sys.list_runner_functions")[target]

    runner_doc = local.cmd(target, "sys.runner_doc")[target]

    for func in runner_func:
        desc = runner_doc[func]

        Functions.objects.update_or_create(
            name=func, type="runner", description=desc or ""
        )
    wheel_docs = runner.cmd("doc.wheel")
    for fun, doc in wheel_docs.items():
        Functions.objects.update_or_create(
            name=fun, type="wheel", description=doc or ""
        )
    return {"something": "useful"}


def manage_key(action, target, kwargs):
    # TODO: CHECK!
    return wheel.cmd("key.{}".format(action), [target], kwarg=kwargs)


def refresh_schedules(minion=None):
    minion = minion or "*"
    api_ret = local.cmd(minion, "schedule.list", kwarg={"return_yaml": False})
    for minion_id in api_ret:
        minion_jobs = api_ret[minion_id]
        Schedule.objects.filter(minion=minion_id).delete()
        for job_name in minion_jobs:
            if job_name != "schedule":
                Schedule.objects.create(
                    minion=minion_id,
                    name=job_name,
                    job=json.dumps(minion_jobs[job_name]),
                )
    return api_ret


def manage_schedules(action, name, minion):
    api_ret = local.cmd(minion, "schedule.{}".format(action), arg=name)
    for target in api_ret:
        # If action was successful.
        if api_ret[target]["result"]:
            if "delete" in action:
                Schedule.objects.filter(minion=minion, name=name).delete()
            else:
                try:
                    schedule = Schedule.objects.filter(minion=minion, name=name).get()
                except Schedule.DoesNotExist:
                    # Retry after refreshing schedules for this minion.
                    refresh_schedules(minion)
                    try:
                        schedule = Schedule.objects.filter(
                            minion=minion, name=name
                        ).get()
                    except Schedule.DoesNotExist:
                        return False
                loaded_job = schedule.loaded_job()
                if "enable" in action:
                    loaded_job["enabled"] = True
                elif "disable" in action:
                    loaded_job["enabled"] = False
                schedule.job = json.dumps(loaded_job)
                schedule.save()
