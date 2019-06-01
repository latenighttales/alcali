from django.urls import path
from django.conf.urls import url

from alcali.web.views.functions import run
from alcali.web.views.overviews import (
    index,
    keys,
    events,
    minions,
    minion_detail,
    jobs,
    job_detail,
)
from alcali.web.views.services import (
    event_stream,
    schedule,
    conformity,
    users,
    settings,
    notifications,
    conformity_detail,
)

urlpatterns = [
    url(r"^$", index, name="index"),
    path("run", run, name="run"),
    url(r"^event_stream$", event_stream, name="event_stream"),
    url(r"^schedule$", schedule, name="schedule"),
    url(r"^conformity$", conformity, name="conformity"),
    path("conformity/<str:minion_id>/", conformity_detail, name="conformity_detail"),
    url(r"^keys$", keys, name="keys"),
    url(r"^users$", users, name="users"),
    url(r"^settings$", settings, name="settings"),
    url(r"^events$", events, name="events"),
    url(r"^minions$", minions, name="minions"),
    path("notifications", notifications, name="notifications"),
    path("minions/<str:minion_id>/", minion_detail, name="minion_detail"),
    url(r"^jobs$", jobs, name="job_list"),
    path("jobs/<str:jid>/<str:minion_id>/", job_detail, name="job_detail"),
]
