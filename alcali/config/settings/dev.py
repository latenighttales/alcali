from .base import *

from distutils.util import strtobool

DJANGO_DEBUG = os.environ.get("DJANGO_DEBUG")
if DJANGO_DEBUG:
    try:
        # lower('y', 'yes', 't', 'true', 'on', '1')
        DJANGO_DEBUG = strtobool(DJANGO_DEBUG)
    # None, empty, bool...
    except (AttributeError, TypeError, ValueError):
        DJANGO_DEBUG = False
else:
    DJANGO_DEBUG = False
DEBUG = DJANGO_DEBUG

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ("debug_toolbar", "django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
]

INTERNAL_IPS = [os.environ.get("DJANGO_INTERNAL_IPS", "127.0.0.1")]

ALLOWED_HOSTS = ["*"]
