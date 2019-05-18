#!/usr/bin/env python
import os
import sys
import dotenv

# Get Django environment
DJANGO_SETTINGS = os.environ.get('DJANGO_SETTINGS', 'alcali.config.settings.dev')

if __name__ == '__main__':
    # This file is static and lives in django directory, so use it as root to
    # determine .env location
    file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
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
