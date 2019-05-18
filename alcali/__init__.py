#!/usr/bin/env python
import os
import sys
import dotenv

# Get Django environment
DJANGO_SETTINGS = os.environ.get('DJANGO_SETTINGS', 'alcali.config.settings.dev')

def manage():
    # This file is copied to ~/.pyenv/versions/3.7.3/lib/python3.7/site-packages
    # during pip install, so use getcwd() to determine .env location
    file = os.path.join(os.getcwd(), '.env')
    dotenv.read_dotenv(file)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
