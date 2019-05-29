"""config URL Configuration
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r"^", include("alcali.web.urls")),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        {"next_page": settings.LOGOUT_REDIRECT_URL},
        name="logout",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "alcali.web.views.services.handler404"
handler500 = "alcali.web.views.services.handler500"

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:  # pragma: no cover
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
