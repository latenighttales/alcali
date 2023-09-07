import os

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from django.contrib import admin

from api.views.salt import (
    SaltReturnsList,
    SaltReturnsRetrieve,
    EventsViewSet,
    jobs_filters,
    job_rendered,
    SaltReturnsListJid,
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
    verify,
    version,
    JobTemplateViewSet,
    social,
    DeviceViewSet,
    DeviceGroupViewSet
)
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

# Create a schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="RDW Api",
        default_version="v1",
        description="RDW API documentation",
        terms_of_service="",
        contact=openapi.Contact(email="anton@griev.ru"),
        license=openapi.License(name="Not Opensource"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
router.register(r"job_templates", JobTemplateViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'device-groups', DeviceGroupViewSet)

urlpatterns = [
    path("", index_view, name="index"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("api/search/", search, name="search"),
    path("api/stats/", stats, name="stats"),
    path("api/version/", version, name="version"),
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
    path("api/jobs/<str:jid>/", SaltReturnsListJid.as_view(), name="jobs-list-jid"),
    path(
        "api/jobs/<str:jid>/<str:minion_id>/rendered_state/",
        job_rendered,
        name="jobs-detail-rendered",
    ),
    path("api/jobs/graph", jobs_graph, name="jobs_graph"),
]

if os.environ.get("SALT_AUTH") == "rest":
    urlpatterns += [path("api/token/verify/", verify, name="token_verify")]

if os.environ.get("AUTH_BACKEND") and os.environ["AUTH_BACKEND"].lower() == "social":
    from rest_social_auth.views import SocialJWTPairUserAuthView

    urlpatterns += [
        path("api/social/", social, name="social"),
        path(
            "api/social/login/",
            SocialJWTPairUserAuthView.as_view(),
            name="social_login",
        ),
    ]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]