"""
Django settings for Alcali project.

"""
import errno
import os

# If there's our env var, it means that env file was loaded somehow(docker).
from os.path import join
from pathlib import Path
from distutils.util import strtobool

from dotenv import load_dotenv

DB_BACKEND = os.environ.get("DB_BACKEND")
if not DB_BACKEND:
    # Load env file
    ENV_PATH = os.environ.get("ENV_PATH", os.getcwd())
    if not ENV_PATH:
        raise FileNotFoundError("ENV_PATH is not set")
    dotenv_path = join(ENV_PATH, ".env")
    env_file = Path(dotenv_path)
    if not env_file.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), env_file)
    load_dotenv(dotenv_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
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

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "127.0.0.1")]

# Application definition

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # TODO: check priority
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "dist")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.{}".format(os.environ["DB_BACKEND"]),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# Place static in the same location as webpack build files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "dist", "static")
STATICFILES_DIRS = []

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
}
# CORS_URLS_REGEX = r'^/api/.*$'
# CORS_ORIGIN_WHITELIST = [
#     "http://127.0.0.1:8001"
# ]

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1)}

# # TODO!
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {"console": {"class": "logging.StreamHandler"}},
#     "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
# }
#
# Get version from file.
try:
    with open(os.path.join(BASE_DIR, "VERSION"), "r") as fh:
        VERSION = fh.read()
except FileNotFoundError:
    VERSION = "unknown"

# LDAP Authentication.
if os.environ.get("AUTH_BACKEND") and os.environ["AUTH_BACKEND"].lower() == "ldap":
    from .ldap_config import *

# Social Authentication.
if os.environ.get("AUTH_BACKEND") and os.environ["AUTH_BACKEND"].lower() == "social":
    INSTALLED_APPS += ["social_django", "rest_social_auth"]
    from .social_config import *
