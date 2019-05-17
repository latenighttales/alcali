from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# INSTALLED_APPS += ('debug_toolbar', 'django_extensions',)
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django_currentuser.middleware.ThreadLocalUserMiddleware',
# ]

INTERNAL_IPS = ['127.0.0.1', '172.18.0.1']
