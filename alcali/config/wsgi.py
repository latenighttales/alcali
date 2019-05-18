"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application

# Get Django environment
DJANGO_SETTINGS = os.environ.get('DJANGO_SETTINGS', 'alcali.config.settings.dev')

# This file is copied to ~/.pyenv/versions/3.7.3/lib/python3.7/site-packages
# during pip install, so use getcwd() to determine .env location
file = os.path.join(os.getcwd(), '.env')
dotenv.read_dotenv(file)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS)

application = get_wsgi_application()
