import os
import json
from urllib.error import URLError

import urllib3

from django.contrib.auth.models import User
from pepper import Pepper, PepperException
from django_currentuser.middleware import get_current_user

from ..utils.input import RawCommand
from ..models import Minions, Functions, MinionsCustomFields, Keys, Schedule

urllib3.disable_warnings()

url = os.environ.get("SALT_URL", "https://127.0.0.1:8080")


def api_connect():
    user = get_current_user()
    api = Pepper(url, ignore_ssl_errors=True)
    try:
        login_ret = api.login(
            str(user.username),
            user.user_settings.token,
            os.environ.get("SALT_AUTH", "alcali"),
        )
    except URLError:
        raise PepperException("URL Error")
    user.user_settings.salt_permissions = json.dumps(login_ret["perms"])
    user.save()
    return api


def get_keys(refresh=False):
    if refresh:
        # Salt return to minion status.
        minion_status = {
            "minions_rejected": "rejected",
            "minions_denied": "denied",
            "minions_pre": "unaccepted",
            "minions": "accepted",
        }

        try:
            api = api_connect()
            api_ret = api.wheel("key.list_all")["return"][0]["data"]["return"]
        except PepperException as e:
            return {"error": str(e)}

        Keys.objects.all().delete()
        for key, value in minion_status.items():
            for minion in api_ret[key]:
                finger_ret = api.wheel("key.finger", match=minion, hash_type="sha256")[
                    "return"
                ][0]["data"]["return"][key]
                obj, created = Keys.objects.update_or_create(
                    minion_id=minion,
                    defaults={"status": value, "pub": finger_ret[minion]},
                )
                if created:
                    pass
                    # LOG CREATED

    return {"result": "refreshed"}


def refresh_minion(minion_id):
    try:
        api = api_connect()
        grain = api.local(minion_id, "grains.items")
    except PepperException as e:
        return {"error": str(e)}
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
            command = RawCommand("salt {} {}".format(minion_id, field["function"]))
            custom_field_return = run_raw(command.parse())
            if "error" in custom_field_return:
                return custom_field_return
            MinionsCustomFields.objects.update_or_create(
                name=field["name"],
                function=field["function"],
                minion=Minions.objects.get(minion_id=minion_id),
                defaults={"value": json.dumps(custom_field_return[minion_id])},
            )
    return {"result": "{} refreshed".format(minion_id)}


def run_raw(load):
    try:
        api = api_connect()
        api_ret = api.low(load)
    except PepperException as e:
        return {"error": str(e)}
    api_ret = api_ret["return"][0]
    return api_ret


def get_events():
    api = Pepper(url, ignore_ssl_errors=True)
    # TODO: find a way.
    user = User.objects.first()
    api.login(
        str(user.username),
        user.user_settings.token,
        os.environ.get("SALT_AUTH", "alcali"),
    )
    response = api.req_stream("/events")
    return response


def init_db(target):
    try:
        api = api_connect()
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
    except PepperException as e:
        return {"error": str(e)}
    return {"result": "refreshed modules using {}".format(target)}


def manage_key(action, target, kwargs):
    try:
        api = api_connect()
        response = api.wheel("key.{}".format(action), match=target, **kwargs)
    except PepperException as e:
        return {"error": str(e)}
    return response


def refresh_schedules(minion=None):
    minion = minion or "*"
    try:
        api = api_connect()
        api_ret = api.local(minion, "schedule.list", kwarg={"return_yaml": False})
    except PepperException as e:
        return {"error": str(e)}
    for minion_id in api_ret["return"][0]:
        # TODO: error mgmt
        minion_jobs = api_ret["return"][0][minion_id]
        Schedule.objects.filter(minion=minion_id).delete()
        for job_name in minion_jobs:
            if job_name != "schedule":
                Schedule.objects.create(
                    minion=minion_id,
                    name=job_name,
                    job=json.dumps(minion_jobs[job_name]),
                )
    return api_ret["return"][0]


def manage_schedules(action, name, minion):
    try:
        api = api_connect()
        api_ret = api.local(minion, "schedule.{}".format(action), arg=name)
    except PepperException as e:
        return {"error": str(e)}
    for target in api_ret["return"][0]:
        # If action was successful.
        if api_ret["return"][0][target]["result"]:
            if "delete" in action:
                Schedule.objects.filter(minion=minion, name=name).delete()
            else:
                try:
                    schedule = Schedule.objects.filter(minion=minion, name=name).get()
                except Schedule.DoesNotExist:
                    # Retry after refreshing schedules for this minion.
                    ret = refresh_schedules(minion)
                    if "error" in ret:
                        return ret
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
    return {"result": "ok"}
