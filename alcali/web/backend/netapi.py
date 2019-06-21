import os
import json
from contextlib import contextmanager
from urllib.error import URLError

import pendulum
from pepper import Pepper, PepperException
from django_currentuser.middleware import get_current_user

from ..utils.input import RawCommand
from ..models.alcali import Minions, Functions, MinionsCustomFields, Keys, Schedule

url = os.environ.get("SALT_URL")


@contextmanager
def api_connect():
    user = get_current_user()
    api = Pepper(url, ignore_ssl_errors=True)
    try:
        login_ret = api.login(
            str(user.username), user.user_settings.token, os.environ.get("SALT_AUTH")
        )
        user.user_settings.salt_permissions = json.dumps(login_ret["perms"])
        user.save()
        yield api

    except (PepperException, ConnectionRefusedError, URLError) as e:
        print("Can't connect to {url}: {e}".format(url=url, e=e))
        yield


def get_keys(refresh=False):
    if refresh:
        # Salt return to minion status.
        minion_status = {
            "minions_rejected": "rejected",
            "minions_denied": "denied",
            "minions_pre": "unaccepted",
            "minions": "accepted",
        }

        with api_connect() as api:
            api_ret = api.wheel("key.list_all")
            api_ret = api_ret["return"][0]["data"]["return"]

            Keys.objects.all().delete()
            for key, value in minion_status.items():
                for minion in api_ret[key]:
                    finger_ret = api.wheel(
                        "key.finger", match=minion, hash_type="sha256"
                    )
                    finger_ret = finger_ret["return"][0]["data"]["return"][key]
                    obj, created = Keys.objects.update_or_create(
                        minion_id=minion,
                        defaults={"status": value, "pub": finger_ret[minion]},
                    )
                    if created:
                        pass
                        # LOG CREATED

    return Keys.objects.all()


def refresh_minion(minion_id):
    with api_connect() as api:
        grain = api.local(minion_id, "grains.items")
        grain = grain["return"][0]
        # TODO: return smt useful, better error mgmt.
        if grain.get(minion_id):
            pillar = api.local(minion_id, "pillar.items")
            pillar = pillar["return"][0]
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
                name = field["name"]
                func = field["function"]
                comm_inst = RawCommand("salt {} {}".format(minion_id, func))
                parsed = comm_inst.parse()
                custom_field_return = run_raw(parsed)
                MinionsCustomFields.objects.update_or_create(
                    name=name,
                    function=func,
                    minion=Minions.objects.get(minion_id=minion_id),
                    defaults={"value": json.dumps(custom_field_return[minion_id])},
                )


def run_job(tgt, fun, args, kwargs=None):
    with api_connect() as api:
        api_ret = api.local(tgt, fun, arg=args, kwarg=kwargs)
    api_ret = api_ret["return"][0]
    return api_ret


def run_raw(load):
    with api_connect() as api:
        api_ret = api.low(load)
    api_ret = api_ret["return"][0]
    return api_ret


def run_runner(fun, args, kwargs=None):
    with api_connect() as api:
        api_ret = api.runner(fun, arg=args, kwarg=kwargs)
    api_ret = api_ret["return"][0]
    return api_ret


def run_wheel(fun, args, kwarg=None, **kwargs):
    with api_connect() as api:
        api_ret = api.wheel(fun, arg=args, kwarg=kwarg, **kwargs)
    api_ret = api_ret["return"][0]
    return api_ret


def get_events():
    with api_connect() as api:
        response = api.req_stream("/events")
    return response


def init_db(target):
    with api_connect() as api:
        # Modules.
        modules_func = api.local(target, "sys.list_functions")
        modules_func = modules_func["return"][0][target]

        modules_doc = api.local(target, "sys.doc")

        for func in modules_func:
            desc = modules_doc["return"][0][target][func]

            Functions.objects.update_or_create(
                name=func, type="local", description=desc or ""
            )
        # Runner.
        # TODO: Factorize.
        runner_func = api.local(target, "sys.list_runner_functions")
        runner_func = runner_func["return"][0][target]

        runner_doc = api.local(target, "sys.runner_doc")

        for func in runner_func:
            desc = runner_doc["return"][0][target][func]

            Functions.objects.update_or_create(
                name=func, type="runner", description=desc or ""
            )
        wheel_docs = api.runner("doc.wheel")
        wheel_docs = wheel_docs["return"][0]
        for fun, doc in wheel_docs.items():
            Functions.objects.update_or_create(
                name=fun, type="wheel", description=doc or ""
            )
    return {"something": "useful"}


def manage_key(action, target, kwargs):
    with api_connect() as api:
        response = api.wheel("key.{}".format(action), match=target, **kwargs)
    return response


def set_perms():
    try:
        user = get_current_user()
        api = Pepper(url, ignore_ssl_errors=True)
        login_ret = api.login(
            str(user.username), user.user_settings.token, os.environ.get("SALT_AUTH")
        )
        user.user_settings.salt_permissions = json.dumps(login_ret["perms"])
        user.save()
    except URLError:
        pass


def refresh_schedules(minion=None):
    minion = minion or "*"
    with api_connect() as api:
        api_ret = api.local(minion, "schedule.list", kwarg={"return_yaml": False})
    for minion_id in api_ret["return"][0]:
        # TODO: error mgmt
        minion_jobs = api_ret["return"][0][minion_id]
        Schedule.objects.filter(minion=minion_id).delete()
        for job_name in minion_jobs:
            Schedule.objects.create(
                minion=minion_id, name=job_name, job=json.dumps(minion_jobs[job_name])
            )
    return api_ret["return"][0]


def manage_schedules(action, name, minion):
    with api_connect() as api:
        api_ret = api.local(minion, "schedule.{}".format(action), arg=name)
    for target in api_ret["return"][0]:
        # If action was successful.
        if api_ret["return"][0][target]["result"]:
            if "delete" in action:
                Schedule.objects.filter(minion=minion, name=name).delete()
            else:
                try:
                    sched = Schedule.objects.filter(minion=minion, name=name).get()
                except Schedule.DoesNotExist:
                    refresh_schedules(minion)
                    try:
                        sched = Schedule.objects.filter(minion=minion, name=name).get()
                    except Schedule.DoesNotExist:
                        return False
                loaded_job = sched.loaded_job()
                if "enable" in action:
                    loaded_job["enabled"] = True
                elif "disable" in action:
                    loaded_job["enabled"] = False
                sched.job = json.dumps(loaded_job)
                sched.save()


def create_schedules(
    target,
    *args,
    function=None,
    cron=None,
    once=None,
    once_fmt=None,
    name=None,
    **kwargs
):
    name = name or pendulum.now().format("YYYYMMDDHHmmss")
    comm_inst = RawCommand(
        "salt {} schedule.add {} function='{}'".format(target, name, function)
    )
    parsed = comm_inst.parse()
    if args:
        parsed[0]["arg"].append("job_args={}".format(args))
    if kwargs:
        parsed[0]["arg"].append("job_kwargs={}".format(kwargs))
    if cron:
        parsed[0]["arg"].append("cron={}".format(cron))
    if once and once_fmt:
        parsed[0]["arg"].append("once={}".format(once))
        parsed[0]["arg"].append("once_fmt={}".format(once_fmt))
    ret = run_raw(parsed)
    return ret
