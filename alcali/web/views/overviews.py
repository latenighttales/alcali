import json
from collections import Counter

import yaml
from ansi2html import Ansi2HTMLConverter
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from ..backend.netapi import refresh_minion, get_keys, set_perms
from ..models.salt import SaltReturns, SaltEvents, Jids
from ..models.alcali import Schedule, Keys, Minions, MinionsCustomFields
from ..utils import graph_data, render_conformity
from ..utils.output import highstate_output, nested_output


@login_required
def index(request):
    """
    Dashboard view.
    :param request:
    :return:
    """

    # On login, get salt permission for user from salt-api.
    set_perms()

    # Update graph data with filters.
    if request.POST.get("period"):
        period_req = request.POST["period"]
        filter_req = request.POST.get("filter")
        days, count, error_count = graph_data(int(period_req), fun=filter_req)
        return JsonResponse({"labels": days, "series": [count, error_count]})

    # Status widget.
    jobs_nb = SaltReturns.objects.count()
    events_nb = SaltEvents.objects.count()
    schedules_nb = Schedule.objects.count()

    # Key widget.
    keys_status = list(Keys.objects.values_list("status", flat=True))
    keys_length = len(keys_status)
    keys_status = dict(Counter(keys_status))

    # Conformity widget.
    minions_all = Minions.objects.all()
    total_minions = len(minions_all)
    conform_minions = [i.minion_id for i in minions_all if i.conformity()]
    conflict_minions = [i.minion_id for i in minions_all if i.conformity() is False]
    # TODO Make a func and accept str, list, dict
    highstate_conformity = {
        "conform": len(conform_minions),
        "conflict": len(conflict_minions),
        "unknown": total_minions - (len(conform_minions) + len(conflict_minions)),
    }

    conformity_name, conformity_data, _ = render_conformity()
    conformity_name.insert(0, "HIGHSTATE")
    conformity_data.insert(0, highstate_conformity)

    return render(
        request,
        "index.html",
        {
            "conformity": conformity_data,
            "conformity_name": conformity_name,
            "total_minions": total_minions,
            "keys_status": keys_status,
            "jobs_nb": jobs_nb,
            "events_nb": events_nb,
            "schedules_nb": schedules_nb,
            "total_keys": keys_length,
        },
    )


@login_required
def jobs(request):
    """
    :param request:
    :return:
    """

    # Filter jobs.
    if request.POST:
        minion = request.POST.get("minion")
        user = request.POST.get("user")
        limit = int(request.POST.get("limit", 100))
        date = request.POST.get("date")
        qry = {}

        # Either date or date range.
        if date:
            date = date.split(" ")[::2]
            if len(date) > 1:
                qry["alter_time__date__range"] = date
            else:
                qry["alter_time__date"] = date[0]

        # Target a minion or some.
        if minion:
            if isinstance(minion, list):
                qry["id__in"] = minion
            else:
                qry["id"] = minion

        filtered_jobs = SaltReturns.objects.filter(**qry).order_by("-alter_time")[
            :limit
        ]

        # Datatable return.
        ret = {"data": []}
        for job in filtered_jobs:
            arguments = ""
            if "fun_args" in job.loaded_ret() and job.loaded_ret()["fun_args"]:
                arguments = [str(i) for i in job.loaded_ret()["fun_args"]]
            # Filter user if requested.
            if user:
                if job.user() not in user:
                    continue

            ret["data"].append(
                [
                    job.jid,
                    job.id,
                    job.fun,
                    arguments,
                    job.user(),
                    job.success_bool(),
                    job.alter_time,
                    "",
                ]
            )
        return JsonResponse(ret, safe=False)

    # Filter options.
    user_list = list({i.user() for i in Jids.objects.all()})
    minion_list = SaltReturns.objects.values_list("id", flat=True).distinct()

    return render(
        request, "job_list.html", {"user_list": user_list, "minion_list": minion_list}
    )


@login_required
def job_detail(request, jid, minion_id):

    # Retrieve job from database.
    job = SaltReturns.objects.get(jid=jid, id=minion_id)

    # Use different output.
    if job.fun in ["state.apply", "state.highstate"]:
        formatted = highstate_output.output({minion_id: job.loaded_ret()["return"]})
    else:
        formatted = nested_output.output({minion_id: job.loaded_ret()["return"]})

    # Convert it to html.
    conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
    html_detail = conv.convert(formatted, ensure_trailing_newline=True)

    return render(request, "job_detail.html", {"job": job, "html_detail": html_detail})


@login_required
def minions(request):

    # Refresh data.
    if request.POST.get("minion"):
        target = request.POST.get("minion")

        # Delete minion from database.
        if request.POST.get("action") == "delete":
            Minions.objects.filter(minion_id=target).delete()
            return JsonResponse({target: "deleted"})

        # Refresh all minions if key is accepted.
        if target == "*":
            accepted_minions = Keys.objects.filter(status="accepted").values_list(
                "minion_id", flat=True
            )
            for minion in accepted_minions:
                refresh_minion(minion)
            return JsonResponse({"refreshed": [i for i in accepted_minions]})

        # Refresh minion.
        refresh_minion(target)
        return JsonResponse({"refreshed": target})

    # Datatables.
    if request.POST:
        ret = {"data": []}
        minions_data = Minions.objects.all()
        for minion in minions_data:
            grain = minion.loaded_grain()
            last_job = minion.last_job()
            last_highstate = minion.last_highstate()
            if last_highstate:
                last_highstate = last_highstate.alter_time
            ret["data"].append(
                [
                    minion.minion_id,
                    minion.conformity(),
                    grain["fqdn"],
                    grain["os"],
                    grain["oscodename"],
                    grain["kernelrelease"],
                    last_job.fun,
                    last_highstate,
                    "",
                ]
            )
        return JsonResponse(ret, safe=False)

    return render(request, "minion_list.html")


@login_required
def minion_detail(request, minion_id):

    # Update graph data.
    if request.POST.get("period"):
        period_req = request.POST["period"]
        filter_req = request.POST.get("filter")
        days, count, error_count = graph_data(
            int(period_req), id=minion_id, fun=filter_req
        )
        return JsonResponse({"labels": days, "series": [count, error_count]})

    minion = get_object_or_404(Minions, minion_id=minion_id)
    custom_fields = MinionsCustomFields.objects.filter(minion=minion)
    # Remove whitespace from custom fields for JS ids.
    js_custom_fields = [i.name.replace(" ", "") for i in custom_fields]

    grain = minion.loaded_grain()
    last_job = minion.last_job()
    last_highstate = minion.last_highstate()
    minion_conformity = minion.conformity()
    grain_yaml = yaml.dump(grain, default_flow_style=False)
    pillar_yaml = yaml.dump(json.loads(minion.pillar), default_flow_style=False)

    return render(
        request,
        "minion_detail.html",
        {
            "minion_id": minion_id,
            "last_job": last_job,
            "last_highstate": last_highstate,
            "conformity": minion_conformity,
            "custom_fields": custom_fields,
            "custom_fields_list": js_custom_fields,
            "grain": grain,
            "grain_yaml": grain_yaml,
            "pillar": pillar_yaml,
        },
    )


@login_required
def keys(request):

    # Refresh button.
    if request.POST.get("action") == "refresh":
        get_keys(refresh=True)
        return JsonResponse({"refreshed": True})

    # Datatable.
    if request.POST:
        ret = {"data": []}
        keys_data = Keys.objects.all()
        for key in keys_data:
            ret["data"].append([key.minion_id, key.status, key.pub, ""])
        return JsonResponse(ret, safe=False)

    return render(request, "keys.html")


@login_required
def events(request):
    e_list = SaltEvents.objects.all().order_by("-alter_time")[:100]
    return render(request, "events_list.html", {"events_list": e_list})
