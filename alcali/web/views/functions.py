from ansi2html import Ansi2HTMLConverter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from django.views import View

from ..backend.netapi import run_raw, run_job, run_runner, run_wheel, manage_key
from ..models.alcali import Functions, Minions
from ..utils import check_permission
from ..utils.output import RawCommand, highstate_output, nested_output


@login_required
def run(request):
    # Fill form with get params.
    optional_get_params = 'null'
    if request.GET:
        optional_get_params = dict(request.GET)

    # Raw command
    if request.POST.get('command'):
        command = request.POST.get('command')
        comm_inst = RawCommand(command)
        parsed = comm_inst.parse()
        ret = run_raw(parsed)
        formatted = '\n'
        if parsed[0]['fun'] in ['state.apply', 'state.highstate']:
            for k, v in ret.items():
                minion_ret = highstate_output.output({k: v})
                formatted += minion_ret + '\n\n'
        else:
            for k, v in ret.items():
                minion_ret = nested_output.output({k: v})
                formatted += minion_ret + '\n\n'
        conv = Ansi2HTMLConverter(inline=False, scheme='xterm')
        html = conv.convert(formatted, ensure_trailing_newline=True)
        return HttpResponse(html)

    # Tooltip function documentation.
    if request.POST.get('tooltip'):
        try:
            desc = Functions.objects.filter(
                name=request.POST.get('tooltip')).values_list('description', flat=True)
            desc = desc[0]
        except IndexError:
            return JsonResponse({})
        return JsonResponse({"desc": desc})

    if request.POST.get('minion_list') and request.POST.get('function_list'):
        # TODO: re implement
        # if request.POST.get('schedule', None):
        #     request_data = request.POST
        #     schedule_return = schedule_run(request_data)
        #     return HttpResponse(yaml.dump(schedule_return, default_flow_style=False))
        tgt_type = request.POST.get('target-type')
        tgt = request.POST['minion_list']
        fun = request.POST['function_list']
        args = ()
        kwargs = {}

        # Dry run button
        if request.POST.get('test'):
            kwargs['test'] = True

        # Arguments
        if request.POST.get('args') and request.POST['args'] != '':
            args = [request.POST['args']]

        # Kwargs
        if request.POST.get('keyword') and request.POST.get('argument'):
            kwargs.update({request.POST['keyword']: request.POST['argument']})

        try:
            ret = run_job(tgt, fun, args, kwargs=kwargs)
            formatted = '\n'
            if fun in ['state.apply', 'state.highstate']:
                for k, v in ret.items():
                    minion_ret = highstate_output.output({k: v})
                    formatted += minion_ret + '\n\n'
            else:
                for k, v in ret.items():
                    minion_ret = nested_output.output({k: v})
                    formatted += minion_ret + '\n\n'
            conv = Ansi2HTMLConverter(inline=False, scheme='xterm')
            html = conv.convert(formatted, ensure_trailing_newline=True)
            return HttpResponse(html)
        # except SaltReqTimeoutError:
        except ZeroDivisionError:
            return JsonResponse({"Error": "SaltReqTimeoutError"})

    # Function list.
    funct_list = Functions.objects.filter(type='modules').values_list(
        'name', flat=True).order_by('name')

    # Nodegroups from master config.
    # nodegroups = opts['nodegroups']
    nodegroups = []

    job_return = None

    # Minion list.
    minion_list = Minions.objects.all().values_list('minion_id', flat=True)

    return render(request, "run.html", {'funct_list': funct_list,
                                        'nodegroups': nodegroups,
                                        'get_params': optional_get_params,
                                        'minion_list': minion_list,
                                        'job_return': job_return})


@login_required
@check_permission
def runner(request):
    if request.POST and request.POST.get('tooltip'):
        desc = Functions.objects.filter(
            name=request.POST.get('tooltip')).values_list('description', flat=True)
        return JsonResponse({"desc": desc[0]})
    if request.POST.get('function_list'):
        fun = request.POST['function_list']
        args = ()
        kwargs = {}

        # Dry run button
        if request.POST.get('test'):
            kwargs['test'] = True

        # Arguments
        if request.POST.get('args') != '':
            args = [request.POST.get('args')]

        # Kwargs
        if request.POST.get('keyword') and request.POST.get('argument'):
            kwargs.update({request.POST['keyword']: request.POST['argument']})

        try:
            ret = run_runner(fun, args, kwargs=kwargs)

            formatted = '\n'
            for k, v in ret.items():
                minion_ret = nested_output.output({k: v})
                formatted += minion_ret + '\n\n'
            conv = Ansi2HTMLConverter(inline=False, scheme='xterm')
            html = conv.convert(formatted, ensure_trailing_newline=True)
            return HttpResponse(html)
        # except SaltReqTimeoutError:
        except:
            return JsonResponse({"Error": "SaltReqTimeoutError"})

    # Function list.
    funct_list = Functions.objects.filter(type='runner').values_list(
        'name', flat=True).order_by('name')

    # Nodegroups from master config.
    # nodegroups = opts['nodegroups']
    nodegroups = []

    job_return = None

    # Minion list.
    minion_list = Minions.objects.all().values_list('minion_id', flat=True)

    return render(request, "runner.html", {'funct_list': funct_list,
                                           'nodegroups': nodegroups,
                                           'minion_list': minion_list,
                                           'job_return': job_return})


@login_required
@check_permission
def wheel(request):
    if request.POST.get('tooltip'):
        desc = Functions.objects.filter(
            name=request.POST.get('tooltip')).values_list('description', flat=True)
        return JsonResponse({"desc": desc[0]})
    if request.POST.get('action') and request.POST.get('target'):
        action = request.POST['action']
        target = request.POST['target']
        kwargs = None
        if action == 'accept':
            kwargs = {'include_rejected': True, 'include_denied': True}
        elif action == 'reject':
            kwargs = {'include_accepted': True, 'include_denied': True}
        elif action == 'delete':
            kwargs = {}
        response = manage_key(action, target, kwargs)
        return JsonResponse(response)

    if request.POST.get('function_list'):
        fun = request.POST['function_list']
        args = ()
        kwargs = {}

        # Dry run button
        if request.POST.get('test'):
            kwargs['test'] = True

        # Arguments
        if request.POST.get('args') != '':
            args = [request.POST.get('args')]

        # Kwargs
        if request.POST.get('keyword') and request.POST.get('argument'):
            kwargs.update({request.POST['keyword']: request.POST['argument']})

        try:
            ret = run_wheel(fun, args, kwarg=kwargs)

            formatted = '\n'
            for k, v in ret.items():
                minion_ret = nested_output.output({k: v})
                formatted += minion_ret + '\n\n'
            conv = Ansi2HTMLConverter(inline=False, scheme='xterm')
            html = conv.convert(formatted, ensure_trailing_newline=True)
            return HttpResponse(html)
        # except SaltReqTimeoutError:
        except:
            return JsonResponse({"Error": "SaltReqTimeoutError"})

    # Function list.
    funct_list = Functions.objects.filter(type='wheel').values_list(
        'name', flat=True).order_by('name')

    # Minion list.
    minion_list = Minions.objects.all().values_list('minion_id', flat=True)

    return render(request, "wheel.html", {'funct_list': funct_list,
                                          'minion_list': minion_list})

# @method_decorator(login_required, name='dispatch')
# class RunView(View):
#     template_name = 'run.html'
#
#     # Fill form with get params.
#     optional_get_params = 'null'
#
#     # Only "run" view publish jobs, "runner" and "wheel" are run locally.
#     publish = True
#
#     # view specific function.
#     view_func = run_job
#     # view function type
#     func_type = 'modules'
#
#     def get(self, request, *args, **kwargs):
#         # Function list.
#         funct_list = Functions.objects.filter(type=self.func_type).values_list(
#             'name', flat=True).order_by('name')
#
#         optional_get_params = dict(request.GET)
#         # Nodegroups from master config.
#         # nodegroups = opts['nodegroups']
#         nodegroups = []
#
#         job_return = None
#
#         # Minion list.
#         minion_list = Minions.objects.all().values_list('minion_id', flat=True)
#         return render(request, self.template_name, {'funct_list': funct_list,
#                                                     'nodegroups': nodegroups,
#                                                     'get_params': optional_get_params,
#                                                     'minion_list': minion_list,
#                                                     'job_return': job_return})
#
#     def post(self, request):
#         # Tooltip function documentation.
#         if request.POST.get('tooltip'):
#             try:
#                 desc = Functions.objects.filter(
#                     name=request.POST.get('tooltip')).values_list('description',
#                                                                   flat=True)
#                 desc = desc[0]
#             except IndexError:
#                 return JsonResponse({"desc": "Something went wrong..."})
#             return JsonResponse({"desc": desc})
#
#         # Raw command
#         if request.POST.get('command'):
#             command = request.POST.get('command')
#             comm_inst = RawCommand(command)
#             parsed = comm_inst.parse()
#             fun = parsed[0]['fun']
#             ret = run_raw(parsed)
#
#         # Run job.
#         if request.POST.get('function_list'):
#             fun = request.POST['function_list']
#             args = ()
#             kwargs = {}
#
#             # Dry run button
#             if request.POST.get('test'):
#                 kwargs['test'] = True
#
#             # Arguments
#             if request.POST.get('args') and request.POST['args'] != '':
#                 args = [request.POST['args']]
#
#             # Kwargs
#             if request.POST.get('keyword') and request.POST.get('argument'):
#                 kwargs.update({request.POST['keyword']: request.POST['argument']})
#
#             if self.publish:
#                 tgt_type = request.POST.get('target-type')
#                 tgt = request.POST['minion_list']
#                 print(kwargs)
#                 ret = run_job(tgt, fun, args, kwargs=kwargs)
#             else:
#                 ret = self.view_func(fun, args, kwargs=kwargs)
#
#         # Return job.
#         formatted = '\n'
#         if self.publish and fun in ['state.apply', 'state.highstate']:
#             for k, v in ret.items():
#                 minion_ret = highstate_output.output({k: v})
#                 formatted += minion_ret + '\n\n'
#         else:
#             for k, v in ret.items():
#                 minion_ret = nested_output.output({k: v})
#                 formatted += minion_ret + '\n\n'
#
#         conv = Ansi2HTMLConverter(inline=False, scheme='xterm')
#         html = conv.convert(formatted, ensure_trailing_newline=True)
#         return HttpResponse(html)
#
#
# @method_decorator(login_required, name='dispatch')
# class RunnerView(RunView):
#     template_name = 'runner.html'
#     publish = False
#     view_func = run_runner
#     func_type = 'runner'
#
