#!/usr/bin/env python
import os
import sys

DJANGO_SETTINGS = os.environ.get("DJANGO_SETTINGS", "config.settings")


def manage():  # pragma: no cover
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
