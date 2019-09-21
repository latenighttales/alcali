from ansi2html import Ansi2HTMLConverter
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import SaltReturns, SaltEvents, Jids
from api.serializers import SaltReturnsSerializer, EventsSerializer
from api.utils.output import highstate_output, nested_output


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class SaltReturnsList(generics.ListAPIView):
    serializer_class = SaltReturnsSerializer

    def get_queryset(self):
        queryset = SaltReturns.objects.all()
        qry = {}
        start = self.request.query_params.get("start", None)
        end = self.request.query_params.get("end", None)
        limit = int(self.request.query_params.get("limit", 200))
        target = self.request.query_params.getlist("target[]")
        users = self.request.query_params.getlist("users[]", None)
        if target:
            if len(target) > 1:
                qry["id__in"] = target
            else:
                qry["id"] = target[0]
        if start and end:
            qry["alter_time__date__range"] = [start, end]

        queryset = queryset.filter(**qry).order_by("-alter_time")[:limit]
        if users:
            queryset = [i for i in queryset if i.user() in users]
        return queryset


@api_view(["GET"])
def jobs_filters(request):
    # Filter options.
    user_list = list({i.user() for i in Jids.objects.all()})
    minion_list = SaltReturns.objects.values_list("id", flat=True).distinct()
    return Response({"users": user_list, "minions": minion_list})


class SaltReturnsRetrieve(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = SaltReturns.objects.all().order_by("-alter_time")
    serializer_class = SaltReturnsSerializer
    lookup_fields = ["jid", "id"]


@api_view(["GET"])
def job_rendered(request, jid, minion_id):
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
    return Response(html_detail)


class EventsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """

    queryset = SaltEvents.objects.all().order_by("-alter_time")[:200]
    serializer_class = EventsSerializer
