import datetime
import json
from collections import Counter, OrderedDict

from ansi2html import Ansi2HTMLConverter
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import (
    HttpResponse,
    JsonResponse,
    StreamingHttpResponse,
    HttpResponseRedirect,
)
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import (
    action,
    api_view,
    renderer_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.backend.netapi import (
    refresh_minion,
    manage_key,
    get_events,
    init_db,
    refresh_schedules,
    run_raw,
    get_keys,
    manage_schedules,
)
from api.models import SaltReturns, Keys, Minions, SaltEvents, Schedule, Conformity
from api.models import UserSettings, MinionsCustomFields, Functions, JobTemplate
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from api.renderer import StreamingRenderer
from api.serializers import (
    ConformitySerializer,
    UsersSerializer,
    UserSettingsSerializer,
    MinionsCustomFieldsSerializer,
    FunctionsSerializer,
    ScheduleSerializer,
    MyTokenObtainPairSerializer,
    SaltReturnsSerializer,
    JobTemplateSerializer,
)
from api.serializers import KeysSerializer, MinionsSerializer
from api.utils import graph_data, render_conformity, RawCommand
from api.utils.output import highstate_output, nested_output

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))


class KeysViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Keys.objects.all()
    serializer_class = KeysSerializer

    @action(methods=["POST"], detail=False)
    def refresh(self, request):
        ret = get_keys(refresh=True)
        if "error" in ret:
            return Response(ret["error"], status=401)
        return Response(ret)

    @action(detail=False)
    def keys_status(self, request):
        keys_status = list(Keys.objects.values_list("status", flat=True))
        keys_status = dict(Counter(keys_status))
        od = OrderedDict()
        for status in ["accepted", "rejected", "denied", "unaccepted"]:
            if status not in keys_status:
                od[status] = 0
            else:
                od[status] = keys_status[status]
        return Response(od)

    @action(methods=["post"], detail=False)
    def manage_keys(self, request):
        kwargs = {}
        key = request.data.get("target")
        key_action = request.data.get("action")
        if key_action == "accept":
            kwargs = {"include_rejected": True, "include_denied": True}
        elif key_action == "reject":
            kwargs = {"include_accepted": True, "include_denied": True}
        ret = manage_key(key_action, key, kwargs)
        if "error" in ret:
            return Response(ret["error"], status=401)
        return Response({"result": "{} on {}: done".format(key_action, key)})


class MinionsViewSet(viewsets.ModelViewSet):
    queryset = Minions.objects.all()
    serializer_class = MinionsSerializer
    lookup_field = "minion_id"
    lookup_value_regex = "[^/]+"

    @action(detail=False, methods=["post"])
    def refresh_minions(self, request):
        if request.POST.get("minion_id"):
            minion_id = request.POST.get("minion_id")
            ret = refresh_minion(minion_id)
            if "error" in ret:
                return Response(ret["error"], status=401)

            return Response({"result": "refreshed {}".format(minion_id)})

        accepted_minions = Keys.objects.filter(status="accepted").values_list(
            "minion_id", flat=True
        )
        for minion in accepted_minions:
            ret = refresh_minion(minion)
            if "error" in ret:
                return Response(ret["error"], status=401)
        return Response({"refreshed": [i for i in accepted_minions]})

    @action(detail=False)
    def conformity(self, request):
        highstate_conformity = {"conform": 0, "conflict": 0, "unknown": 0}
        for minion in Minions.objects.all():
            if minion.conformity() is True:
                highstate_conformity["conform"] += 1
            elif minion.conformity() is False:
                highstate_conformity["conflict"] += 1
            else:
                highstate_conformity["unknown"] += 1

        conformity_name, conformity_data, _ = render_conformity()
        conformity_name.insert(0, "HIGHSTATE")
        conformity_data.insert(0, highstate_conformity)
        return Response({"name": conformity_name, "data": conformity_data})

    @action(detail=True)
    def conformity_detail(self, request, minion_id):
        minion = self.get_object()

        # Get conformity data.
        _, _, custom_conformity = render_conformity(minion.minion_id)
        custom_conformity = (
            custom_conformity[minion.minion_id] if custom_conformity else None
        )
        minion_conformity = minion.conformity()

        # Convert states to html.
        conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
        last_highstate = minion.last_highstate()
        succeeded, unchanged, failed = {}, {}, {}

        if last_highstate:
            last_highstate = last_highstate.loaded_ret()["return"]
            # Sls error
            if isinstance(last_highstate, list):
                failed = {"error": last_highstate[0]}
            else:
                for state in last_highstate:
                    state_name = state.split("_|-")[1]
                    formatted = highstate_output.output(
                        {minion.minion_id: {state: last_highstate[state]}},
                        summary=False,
                    )
                    if last_highstate[state]["result"] is True:
                        succeeded[state_name] = conv.convert(
                            formatted, ensure_trailing_newline=True
                        )
                    elif last_highstate[state]["result"] is None:
                        unchanged[state_name] = conv.convert(
                            formatted, ensure_trailing_newline=True
                        )
                    else:
                        failed[state_name] = conv.convert(
                            formatted, ensure_trailing_newline=True
                        )
        return Response(
            {
                "custom_conformity": custom_conformity,
                "conformity": minion_conformity,
                "succeeded": succeeded,
                "unchanged": unchanged,
                "failed": failed,
            }
        )


class MinionsCustomFieldsViewSet(viewsets.ModelViewSet):
    queryset = MinionsCustomFields.objects.all()
    serializer_class = MinionsCustomFieldsSerializer

    def perform_create(self, serializer):
        for minion in Minions.objects.all():
            serializer.save(minion=minion)

    @action(methods=["post"], detail=False)
    def delete_field(self, request):
        field = request.data.get("name")
        MinionsCustomFields.objects.filter(name=field).delete()
        return Response({"result": "{} field deleted".format(field)})


class ConformityViewSet(viewsets.ModelViewSet):
    queryset = Conformity.objects.all()
    serializer_class = ConformitySerializer
    lookup_value_regex = "[0-9a-zA-Z.]+"

    @action(detail=False)
    def render(self, request):
        conformity_name = [i.name for i in Conformity.objects.all()]
        default_columns = [
            {"text": "Minion id", "value": "minion_id"},
            {"text": "Last Highstate", "value": "last_highstate"},
            {"text": "Highstate Conformity", "value": "conformity"},
            {"text": "Succeeded", "value": "succeeded"},
            {"text": "Unchanged", "value": "unchanged"},
            {"text": "Failed", "value": "failed"},
        ]
        for conformity in conformity_name:
            default_columns.append({"text": conformity, "value": conformity})

        # Get conformity data.
        _, _, rendered_conformity = render_conformity()
        # Compute number of succeeded, unchanged and failed states.
        conformity_data = []
        minions = Minions.objects.all()
        for minion in minions:
            succeeded, unchanged, failed = 0, 0, 0
            last_highstate = minion.last_highstate()
            if last_highstate:
                last_highstate_date = last_highstate.alter_time
                last_highstate = last_highstate.loaded_ret()["return"]
                # Sls error
                if isinstance(last_highstate, list):
                    succeeded, unchanged, failed = None, None, 1
                else:
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

            default_conformity = {
                "minion_id": minion.minion_id,
                "last_highstate": last_highstate_date,
                "conformity": "Unknown"
                if minion.conformity() is None
                else str(minion.conformity()),
                "succeeded": succeeded,
                "unchanged": unchanged,
                "failed": failed,
            }
            # Add custom conformity values to datatable data.
            if rendered_conformity:
                for conformity in rendered_conformity[minion.minion_id]:
                    default_conformity.update(conformity)
            conformity_data.append(default_conformity)
        return Response({"name": default_columns, "data": conformity_data})


class FunctionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Functions.objects.all()
    serializer_class = FunctionsSerializer


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def list(self, request, *args, **kwargs):
        # Datatable.
        ret = []
        for schedule in Schedule.objects.values():
            for k, v in json.loads(schedule["job"]).items():
                schedule[k] = v
            del schedule["job"]
            ret.append(schedule)
        return Response(ret)

    @action(methods=["POST"], detail=False)
    def refresh(self, request):
        ret = refresh_schedules()
        if "error" in ret:
            return Response(ret["error"], status=401)
        return Response({"result": "refreshed"})

    @action(methods=["POST"], detail=False)
    def manage(self, request):
        action = request.data.get("action")
        minion = request.data.get("minion")
        name = request.data.get("name")
        ret = manage_schedules(action, name, minion)
        if not ret:
            return Response({"result": "not good"})
        if "error" in ret:
            return Response(ret["error"], status=401)
        return Response(
            {"result": "schedule " + name + " on " + minion + " " + action + "d"}
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.all()

    def get_permissions(self):
        permission_classes = []
        # Only Staff users are allowed to create users.
        if self.action == "create":
            permission_classes = [IsAdminUser]
        elif self.action in ["retrieve", "update", "partial_update", "list"]:
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=["POST"], detail=True)
    def manage_token(self, request, pk):
        user = self.get_object()
        action = request.data.get("action")
        if action == "renew":
            user.user_settings.generate_token()
        elif action == "revoke":
            user.user_settings.token = "REVOKED"
            user.user_settings.save()
        return Response({"result": "{} successful".format(action)})


class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer


class JobTemplateViewSet(viewsets.ModelViewSet):
    queryset = JobTemplate.objects.all()
    serializer_class = JobTemplateSerializer


@api_view(["GET"])
def jobs_graph(request):
    id = request.query_params.get("id", None)
    params = {
        "period": int(request.query_params.get("period", 7)),
        "fun": request.query_params.get("fun", "all"),
    }
    if id:
        params.update(id=id)
    days, count, error_count = graph_data(**params)
    return Response({"labels": days, "series": [count, error_count]})


@api_view(["POST"])
def parse_modules(request):
    if request.data.get("target"):
        ret = init_db(request.data.get("target"))
        if "error" in ret:
            return Response(ret["error"], status=401)
        return Response(ret)


@api_view(["GET"])
def search(request):
    if request.query_params.get("q", None):
        query = request.query_params.get("q")
        # First try to match minions.
        minion_results = []
        return_results = []
        minion_query = Minions.objects.filter(minion_id__icontains=query)
        return_query = SaltReturns.objects.filter(
            Q(jid__icontains=query) | Q(fun__icontains=query)
        )[:200]
        if minion_query:
            for res in minion_query:
                minion = MinionsSerializer(res)
                minion_results.append(minion.data)
        if return_query:
            for res in return_query:
                job = SaltReturnsSerializer(res)
                return_results.append(job.data)
        return Response(
            {"minions": minion_results, "jobs": return_results, "query": query}
        )

        # Return to referer
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@api_view(["GET"])
def stats(request):
    # Status widget.
    jobs_nb = SaltReturns.objects.count()
    events_nb = SaltEvents.objects.count()
    schedules_nb = Schedule.objects.count()
    return Response({"jobs": jobs_nb, "events": events_nb, "schedules": schedules_nb})


@api_view(["GET"])
def version(request):
    return Response({"version": settings.VERSION})


@api_view(["GET"])
@renderer_classes([StreamingRenderer])
def event_stream(request):
    # Web socket.
    response = StreamingHttpResponse(
        get_events(), status=200, content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response


@api_view(["POST"])
def run(request):
    if request.POST.get("raw"):
        command = RawCommand(request.POST.get("command"))
        parsed_command = command.parse()
        # Schedules.
        if request.POST.get("schedule_type"):
            schedule_type = request.POST.get("schedule_type")
            schedule_name = request.POST.get(
                "schedule_name", datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            )
            schedule_parsed = [
                {
                    "client": "local",
                    "batch": None,
                    "tgt_type": parsed_command[0]["tgt_type"],
                    "tgt": parsed_command[0]["tgt"],
                    "fun": "schedule.add",
                    "arg": [
                        schedule_name,
                        "function={}".format(parsed_command[0]["fun"]),
                        "job_args={}".format(parsed_command[0]["arg"]),
                    ],
                }
            ]
            if schedule_type == "once":
                schedule_date = request.POST.get("schedule")
                schedule_parsed[0]["arg"].append("once={}".format(schedule_date))
                schedule_parsed[0]["arg"].append("once_fmt=%Y-%m-%d %H:%M:%S")
            else:
                cron = request.POST.get("cron")
                schedule_parsed[0]["arg"].append("cron={}".format(cron))
            ret = run_raw(schedule_parsed)
            if "error" in ret:
                return Response(ret["error"], status=401)
            formatted = nested_output.output(ret)
            conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
            html = conv.convert(formatted, ensure_trailing_newline=True)
            return HttpResponse(html)

        cli_ret = request.POST.get("cli")
        conv = Ansi2HTMLConverter(inline=False, scheme="xterm")
        ret = run_raw(parsed_command)
        if "error" in ret:
            return Response(ret["error"], status=401)
        formatted = "\n"

        # Error.
        if isinstance(ret, str):
            item_ret = nested_output.output(ret)
            formatted += item_ret + "\n\n"
        # runner or wheel client.
        elif isinstance(ret, list):
            for item in ret:
                item_ret = nested_output.output(item)
                formatted += item_ret + "\n\n"
        # Highstate.
        elif (
            parsed_command[0]["fun"] in ["state.apply", "state.highstate"]
            and parsed_command[0]["client"] != "local_async"
        ):
            for state, out in ret.items():
                minion_ret = highstate_output.output({state: out})
                formatted += minion_ret + "\n\n"
        # Everything else.
        else:
            for state, out in ret.items():
                minion_ret = nested_output.output({state: out})
                formatted += minion_ret + "\n\n"

        if cli_ret:
            return JsonResponse({"results": formatted})
        html = conv.convert(formatted, ensure_trailing_newline=True)
        return HttpResponse(html)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def verify(request):
    if request.POST.get("username") and request.POST.get("password"):
        try:
            user = User.objects.get(username=request.POST.get("username"))
        except User.DoesNotExist:
            return HttpResponse("Unauthorized", status=401)
        if request.POST.get("password") == user.user_settings.token:
            return Response({request.POST.get("username"): None})
        return HttpResponse("Unauthorized", status=401)


@api_view(["GET"])
@permission_classes([AllowAny])
def social(request):
    return Response(
        {
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "provider": "google-oauth2",
            "redirect_uri": settings.SOCIAL_AUTH_REDIRECT_URI,
        }
    )
