"""
Django settings for Alcali project.
"""
import os
import errno
from distutils.util import strtobool
from os.path import join
from pathlib import Path

from django.conf.global_settings import DATETIME_INPUT_FORMATS
from dotenv import load_dotenv

# If there's our env var, it means that env file was loaded somehow(docker).
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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATETIME_INPUT_FORMATS += ["%Y, %b %d %H:%M:%S.%f"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

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
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DJANGO_DEBUG

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "127.0.0.1")]
# Application definition

INSTALLED_APPS = [
    "alcali.web.apps.WebConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
]

ROOT_URLCONF = "alcali.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "../web/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "alcali.web.context_processors.notifications",
            ]
        },
    }
]

WSGI_APPLICATION = "alcali.config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.{}".format(
            os.environ.get("DB_BACKEND", "sqlite3")
        ),
        "NAME": os.environ.get("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

MODELS_MANAGED = True

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
WHITENOISE_USE_FINDERS = True

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login"
