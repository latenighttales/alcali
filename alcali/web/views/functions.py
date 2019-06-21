from ansi2html import Ansi2HTMLConverter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from ..backend.netapi import (
    run_raw,
    run_job,
    run_runner,
    run_wheel,
    manage_key,
    create_schedules,
)
from ..models.alcali import Functions, Minions
from ..utils.output import highstate_output, nested_output
from ..utils.input import RawCommand


@login_required
def run(request):
    """
    Run commands.
    :param request:
    :return:
    """
    # Fill form with get params.
    optional_get_params = "null"
    if request.GET:
        optional_get_params = dict(request.GET)

    # Key management.
    if request.POST.get("action") and request.POST.get("target"):
        action = request.POST["action"]
        target = request.POST["target"]
        kwargs = None
        if action == "accept":
            kwargs = {"include_rejected": True, "include_denied": True}
        elif action == "reject":
            kwargs = {"include_accepted": True, "include_denied": True}
        elif action == "delete":
            kwargs = {}
        response = manage_key(action, target, kwargs)
        return JsonResponse(response)

    # Raw command
    if request.POST.get("command"):
        command = request.POST.get("command")
        comm_inst = RawCommand(command)
        parsed = comm_inst.parse()
        ret = run_raw(parsed)
        formatted = "\n"
        if parsed[0]["fun"] in ["state.apply", "state.highstate"]:
            for k, v in ret.items():
                minion_ret = highstate_output.output({k: v})
                formatted += minion_ret + "\n\n"
        else:
            for k, v in ret.items():
                minion_ret = nested_output.output({k: v})
                formatted += minion_ret + "\n\n"
        conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
        html = conv.convert(formatted, ensure_trailing_newline=True)
        return HttpResponse(html)

    # Tooltip function documentation.
    if request.POST.get("tooltip") and request.POST.get("client"):
        try:
            desc = Functions.objects.filter(
                name=request.POST.get("tooltip"), type=request.POST.get("client")
            ).values_list("description", flat=True)
            desc = desc[0]
        except IndexError:
            return JsonResponse({})
        return JsonResponse({"desc": desc})

    if request.POST.get("function_list"):
        client = request.POST.get("client")
        tgt_type = request.POST.get("target-type")
        tgt = request.POST.get("minion_list")
        fun = request.POST["function_list"]
        args = ()
        kwargs = {}

        # Dry run button
        if request.POST.get("test"):
            kwargs["test"] = True

        # Arguments
        if request.POST.get("args") and request.POST["args"] != "":
            args = [request.POST["args"]]

        # Kwargs
        if request.POST.get("keyword") and request.POST.get("argument"):
            kwargs.update({request.POST["keyword"]: request.POST["argument"]})

        # Schedules.
        if request.POST.get("schedule-sw") == "on":
            schedule_type = request.POST.get("schedule_type")
            if schedule_type == "once":
                schedule_date = request.POST.get("schedule")
                schedule_date = "{}:00".format(schedule_date)
                ret = create_schedules(
                    tgt,
                    function=fun,
                    once=schedule_date,
                    once_fmt="%Y-%m-%d %H:%M:%S",
                    *args,
                    **kwargs
                )
            else:
                schedule_cron = request.POST.get("cron")
                ret = create_schedules(
                    tgt, cron=schedule_cron, function=fun, *args, **kwargs
                )
            return HttpResponse(ret)

        if client == "local":
            ret = run_job(tgt, fun, args, kwargs=kwargs)
        elif client == "runner":
            ret = run_runner(fun, args, kwargs=kwargs)
        elif client == "wheel":
            ret = run_wheel(fun, args, kwarg=None, **kwargs)

        formatted = "\n"
        if fun in ["state.apply", "state.highstate"]:
            for k, v in ret.items():
                minion_ret = highstate_output.output({k: v})
                formatted += minion_ret + "\n\n"
        else:
            for k, v in ret.items():
                minion_ret = nested_output.output({k: v})
                formatted += minion_ret + "\n\n"
        conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
        html = conv.convert(formatted, ensure_trailing_newline=True)
        return HttpResponse(html)

    # Functions name.
    # TODO optimise
    funct = Functions.objects.all()
    local_list = [i.name for i in funct if i.type == "local"]
    runner_list = [i.name for i in funct if i.type == "runner"]
    wheel_list = [i.name for i in funct if i.type == "wheel"]

    # Nodegroups from master config.
    nodegroups = []

    job_return = None

    # Minion list.
    minion_list = Minions.objects.all().values_list("minion_id", flat=True)

    return render(
        request,
        "run.html",
        {
            "local_list": local_list,
            "runner_list": runner_list,
            "wheel_list": wheel_list,
            "nodegroups": nodegroups,
            "get_params": optional_get_params,
            "minion_list": minion_list,
            "job_return": job_return,
        },
    )
