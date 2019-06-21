from ansi2html import Ansi2HTMLConverter
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, StreamingHttpResponse  # , HttpResponse
from django.shortcuts import render  # , get_object_or_404

from alcali.web.utils import render_conformity
from alcali.web.utils.output import highstate_output

from ..backend.netapi import (
    get_events,
    refresh_schedules,
    manage_schedules,
    init_db,
    create_schedules,
)
from ..forms import AlcaliUserForm
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


@login_required
def schedule(request):

    # Highstate conformity.
    if request.POST.get("cron"):
        cron = request.POST.get("cron")
        target = request.POST.get("target")
        if not target:
            target = "*"
        ret = create_schedules(
            target,
            function="state.apply",
            cron=cron,
            name="highstate_conformity",
            test=True,
        )
        return JsonResponse({"result": ret})

    if request.POST:

        # Refresh schedules.
        if request.POST.get("action") == "refresh":
            ret = refresh_schedules(minion=request.POST.get("minion"))

            return JsonResponse({"refreshed": ret})

        # Manage schedules. Action could be: delete, disable_job, enable_job.
        if request.POST.get("action") and request.POST.get("name"):
            ret = manage_schedules(
                request.POST.get("action"),
                request.POST.get("name"),
                request.POST.get("minion"),
            )

            return JsonResponse({request.POST.get("action"): ret})

        # Datatable.
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

    # Datatable.
    if request.POST.get("action") == "list":
        ret = {
            "data": [],
            "columns": [
                "Minion id",
                "Last Highstate",
                "Highstate Conformity",
                "succeeded",
                "Unchanged",
                "Failed",
            ],
        }
        conformity_all = Conformity.objects.all()
        # Add custom conformity fields to datatable columns.
        if conformity_all:
            ret["columns"] = ret["columns"] + [i.name for i in conformity_all]

        # Get conformity data.
        _, _, rendered_conformity = render_conformity()

        # Compute number of succeeded, unchanged and failed states.
        minions = Minions.objects.all()
        for minion in minions:
            succeeded, unchanged, failed = 0, 0, 0
            last_highstate = minion.last_highstate()
            if last_highstate:
                last_highstate_date = last_highstate.alter_time
                last_highstate = last_highstate.loaded_ret()["return"]
                for state in last_highstate:
                    if last_highstate[state]["result"] is True:
                        succeeded += 1
                    elif last_highstate[state]["result"] is None:
                        unchanged += 1
                    else:
                        failed += 1
            else:
                last_highstate_date, succeeded, unchanged, failed = (
                    None,
                    None,
                    None,
                    None,
                )

            # Add custom conformity values to datatable data.
            if rendered_conformity:
                custom_conformity = rendered_conformity[minion.minion_id]
                custom_conformity = [list(i.values())[0] for i in custom_conformity]
            else:
                custom_conformity = []
            ret["data"].append(
                [
                    minion.minion_id,
                    last_highstate_date,
                    minion.conformity(),
                    succeeded,
                    unchanged,
                    failed,
                ]
                + custom_conformity
                + [""]
            )

        return JsonResponse(ret, safe=False)

    return render(request, "conformity.html", {})


@login_required
def conformity_detail(request, minion_id):

    minion = Minions.objects.get(minion_id=minion_id)

    # Get conformity data.
    _, _, custom_conformity = render_conformity(minion_id)
    custom_conformity = custom_conformity[minion_id] if custom_conformity else None
    minion_conformity = minion.conformity()

    # Convert states to html.
    conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
    last_highstate = minion.last_highstate()
    succeeded, unchanged, failed = {}, {}, {}

    if last_highstate:
        last_highstate = last_highstate.loaded_ret()["return"]
        for state in last_highstate:
            state_name = state.split("_|-")[1]
            if last_highstate[state]["result"] is True:
                formatted = highstate_output.output(
                    {minion_id: {state: last_highstate[state]}}, summary=False
                )
                succeeded[state_name] = conv.convert(
                    formatted, ensure_trailing_newline=True
                )
            elif last_highstate[state]["result"] is None:
                formatted = highstate_output.output(
                    {minion_id: {state: last_highstate[state]}}, summary=False
                )
                unchanged[state_name] = conv.convert(
                    formatted, ensure_trailing_newline=True
                )
            else:
                formatted = highstate_output.output(
                    {minion_id: {state: last_highstate[state]}}, summary=False
                )
                failed[state_name] = conv.convert(
                    formatted, ensure_trailing_newline=True
                )
    return render(
        request,
        "conformity_detail.html",
        {
            "minion_id": minion_id,
            "custom_conformity": custom_conformity,
            "conformity": minion_conformity,
            "succeeded": succeeded,
            "unchanged": unchanged,
            "failed": failed,
        },
    )


@login_required
def event_stream(request):

    # Web socket.
    response = StreamingHttpResponse(
        get_events(), status=200, content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response


@login_required
def search(request):

    # TODO: search.
    if request.GET.get("q"):
        query = request.GET.get("q")


@user_passes_test(lambda u: u.is_superuser)
def users(request):

    form = AlcaliUserForm()
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

    return render(request, "users.html", {"form": form})


# @user_passes_test(lambda u: u.is_superuser)
# def edit_users(request, username):
#
#     user_to_edit = get_object_or_404(User, username=username)
#     if request.POST.get("action") == "edit":
#         return render(
#             request,
#             "template_users.html",
#             {"form": AlcaliUserChangeForm(instance=user_to_edit)},
#         )
#     if request.method == "POST":
#         form = AlcaliUserChangeForm(request.POST, instance=user_to_edit)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("all good")


@user_passes_test(lambda u: u.is_superuser)
def settings(request):

    user = User.objects.get(username=request.user)

    notifs_status = [
        "notifs_created",
        "notifs_published",
        "notifs_returned",
        "notifs_event",
    ]

    # Delete minion custom field, delete conformity, or init_db.
    if request.POST.get("target"):
        target = request.POST.get("target")
        if request.POST.get("action") == "delete_conformity":
            ret = Conformity.objects.filter(name=target).delete()
        if request.POST.get("action") == "delete_field":
            ret = MinionsCustomFields.objects.filter(name=target).delete()
        if request.POST.get("action") == "init_db":
            init_db(target)

            return JsonResponse({"result": "updated"})

        return JsonResponse({"result": ret})

    # Create minion custom field, create conformity.
    if request.POST.get("name") and request.POST.get("function"):
        name = request.POST.get("name")
        function = request.POST.get("function")

        if request.POST.get("action") == "create_field":
            for minion in Minions.objects.all():
                MinionsCustomFields.objects.create(
                    name=name, function=function, minion=minion, value="{}"
                )

        if request.POST.get("action") == "create_conformity":
            name = request.POST.get("name")
            function = request.POST.get("function")
            Conformity.objects.create(name=name, function=function)

        return JsonResponse({"result": "updated"})

    # User settings.
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
        Functions.objects.filter(type="local")
        .values_list("name", flat=True)
        .order_by("name")
    )
    conformity_fields = Conformity.objects.values("name", "function")
    return render(
        request,
        "settings.html",
        {
            "notifs": current_notifs,
            "max_notifs": int(max_notifs),
            "minion_fields": minion_fields,
            "function_list": funct_list,
            "minion_list": minion_list,
            "conformity_fields": conformity_fields,
        },
    )


def notifications(request):

    # Delete notifications.
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

    # Create notifications.
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


def handler404(request, exception):
    return render(request, "404.html", {"exception": exception}, status=404)


def handler500(request):
    return render(request, "500.html", status=500)
