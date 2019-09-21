from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.salt import (
    SaltReturnsList,
    SaltReturnsRetrieve,
    EventsViewSet,
    jobs_filters,
    job_rendered,
)

from api.views.alcali import (
    index_view,
    KeysViewSet,
    MinionsViewSet,
    jobs_graph,
    stats,
    event_stream,
    parse_modules,
    ConformityViewSet,
    UsersViewSet,
    MinionsCustomFieldsViewSet,
    FunctionsViewSet,
    run,
    UserSettingsViewSet,
    ScheduleViewSet,
    MyTokenObtainPairView,
    search,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"keys", KeysViewSet)
router.register(r"minions", MinionsViewSet)
router.register(r"events", EventsViewSet)
router.register(r"conformity", ConformityViewSet)
router.register(r"users", UsersViewSet)
router.register(r"userssettings", UserSettingsViewSet)
router.register(r"minionsfields", MinionsCustomFieldsViewSet)
router.register(r"functions", FunctionsViewSet)
router.register(r"schedules", ScheduleViewSet)

urlpatterns = [
    path("", index_view, name="index"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("api/search/", search, name="search"),
    path("api/stats/", stats, name="stats"),
    path("api/settings/initdb", parse_modules, name="parse_modules"),
    path("api/event_stream/", event_stream, name="event_stream"),
    path("api/jobs/", SaltReturnsList.as_view(), name="jobs-list"),
    path("api/jobs/filters/", jobs_filters, name="jobs-filters"),
    path("api/run/", run, name="run"),
    path(
        "api/jobs/<str:jid>/<str:id>/",
        SaltReturnsRetrieve.as_view(),
        name="jobs-detail",
    ),
    path(
        "api/jobs/<str:jid>/<str:minion_id>/rendered_state/",
        job_rendered,
        name="jobs-detail-rendered",
    ),
    path("api/jobs/graph", jobs_graph, name="jobs_graph"),
]
