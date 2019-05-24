import json

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse

from ..forms import AlcaliUserForm, AlcaliUserChangeForm
from ..models.alcali import (
    Schedule,
    UserSettings,
    Minions,
    MinionsCustomFields,
    Conformity,
    Keys,
    Functions,
    Notifications,
)

# if settings.ALCALI_BACKEND == 'netapi':
from ..backend.netapi import (
    get_events,
    refresh_schedules,
    manage_schedules,
    init_db,
    create_schedules,
)


# elif settings.ALCALI_BACKEND == 'pyapi':
#    from ..backend.pyapi import run_job
# else:
#    raise ImportError


@login_required
def schedule(request):
    if request.POST:
        if request.POST.get("action") == "refresh":
            ret = refresh_schedules(minion=request.POST.get("minion"))
            return JsonResponse({"refreshed": ret})
        if request.POST.get("action") and request.POST.get("name"):
            ret = manage_schedules(
                request.POST.get("action"),
                request.POST.get("name"),
                request.POST.get("minion"),
            )

            return JsonResponse({request.POST.get("action"): ret})

        ret = {"data": [], "columns": ["target"]}
        schedule_list = Schedule.objects.all()
        for sched in schedule_list:
            data = [sched.minion]
            for key, value in sched.loaded_job().items():
                if key not in ret["columns"]:
                    ret["columns"].append(key)
                data.insert(ret["columns"].index(key), value)
            ret["data"].append(data)

        return JsonResponse(ret, safe=False)

    return render(request, "schedule.html")


@login_required
def conformity(request):
    if request.POST.get("cron"):
        cron = request.POST.get("cron")
        target = request.POST.get("target")
        if not target:
            target = "*"
        create_schedules(target, cron)

    if request.POST.get("action") == "delete_field" and request.POST.get("target"):
        target = request.POST.get("target")
        ret = Conformity.objects.filter(name=target).delete()
        return JsonResponse({"result": ret})

    if request.POST.get("name") and request.POST.get("function"):
        name = request.POST.get("name")
        function = request.POST.get("function")
        Conformity.objects.create(name=name, function=function)
        # TODO: return

    conformity_fields = Conformity.objects.values("name", "function")
    funct_list = (
        Functions.objects.filter(type="modules")
        .values_list("name", flat=True)
        .order_by("name")
    )
    return render(
        request,
        "conformity.html",
        {"conformity_fields": conformity_fields, "function_list": funct_list},
    )


@login_required
def event_stream(request):
    response = StreamingHttpResponse(
        get_events(), status=200, content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response


@login_required
def search(request):
    if request.GET.get("q"):
        query = request.GET.get("q")


@staff_member_required
def users(request):
    form = AlcaliUserForm()
    change_form = AlcaliUserChangeForm()
    if request.method == "POST":
        form = AlcaliUserForm(request.POST)
        if form.is_valid():
            form.save()
    if request.POST.get("action") == "list":
        users = User.objects.all()
        ret = {"data": []}
        for user in users:
            ret["data"].append(
                [
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.user_settings.token,
                    user.user_settings.salt_permissions,
                    user.last_login,
                    "",
                ]
            )
        return JsonResponse(ret, safe=False)

    return render(request, "users.html", {"form": form, "change_form": change_form})


@staff_member_required
def settings(request):
    user = User.objects.get(username=request.user)
    notifs_status = [
        "notifs_created",
        "notifs_published",
        "notifs_returned",
        "notifs_event",
    ]

    if request.POST.get("action") == "init_db" and request.POST.get("target"):
        init_db(request.POST.get("target"))
        return JsonResponse({"result": "updated"})

    if request.POST.get("action") == "delete_field" and request.POST.get("target"):
        target = request.POST.get("target")
        ret = MinionsCustomFields.objects.filter(name=target).delete()
        return JsonResponse({"result": ret})

    if request.POST.get("name") and request.POST.get("function"):
        name = request.POST.get("name")
        function = request.POST.get("function")
        for minion in Minions.objects.all():
            MinionsCustomFields.objects.create(
                name=name, function=function, minion=minion, value="{}"
            )
        return JsonResponse({"result": "updated"})

    if request.POST.get("action") == "notifications":
        user_notifs = {}
        for status in notifs_status:
            if status.split("_")[1] in request.POST:
                user_notifs[status] = True
            else:
                user_notifs[status] = False

        user = UserSettings.objects.get(user=user)
        for k, v in user_notifs.items():
            setattr(user, k, v)
        if request.POST.get("max_notifs"):
            setattr(user, "max_notifs", request.POST.get("max_notifs"))
        user.save()
        return JsonResponse({"result": "updated"})

    current_notifs = UserSettings.objects.filter(user=user).values(*notifs_status)
    max_notifs = UserSettings.objects.filter(user=user).values_list(
        "max_notifs", flat=True
    )[0]
    if not current_notifs:
        # Defaults.
        current_notifs = {
            "notifs_created": False,
            "notifs_published": False,
            "notifs_returned": True,
            "notifs_event": False,
        }
    else:
        current_notifs = current_notifs[0]
    # Format notifs.
    current_notifs = {(k.split("_")[1]): v for k, v in current_notifs.items()}
    # Minion list.
    minion_list = Keys.objects.all().values_list("minion_id", flat=True)
    minion_fields = MinionsCustomFields.objects.values("name", "function").distinct()
    # Function list.
    funct_list = (
        Functions.objects.filter(type="modules")
        .values_list("name", flat=True)
        .order_by("name")
    )
    return render(
        request,
        "settings.html",
        {
            "notifs": current_notifs,
            "max_notifs": int(max_notifs),
            "minion_fields": minion_fields,
            "function_list": funct_list,
            "minion_list": minion_list,
        },
    )


def notifications(request):
    if request.POST.get("action") == "delete":
        notif_id = request.POST.get("id")
        try:
            if notif_id == "*":
                Notifications.objects.all().delete()
            else:
                Notifications.objects.get(id=notif_id).delete()
        # Might be deleted by signal.
        except Notifications.DoesNotExist:
            pass
        return JsonResponse({"result": "success"})
    if request.POST.get("data") and request.POST.get("tag"):
        tag = request.POST.get("tag")
        data = request.POST.get("data")
        notif_type = request.POST.get("type")
        user = User.objects.get(username=request.user)
        notif = Notifications.objects.create(
            data=data, tag=tag, notif_type=notif_type, user=user
        )
        return render(
            request,
            "template_notifs.html",
            {
                "notif_id": notif.id,
                "notif_link": notif.notif_attr()["link"],
                "notif_color": notif.notif_attr()["color"],
                "notif_icon": notif.notif_attr()["icon"],
                "notif_text": notif.notif_attr()["text"],
                "notif_ts": notif.datetime(),
            },
        )
