from django.apps import AppConfig


class WebConfig(AppConfig):
    name = "alcali.web"

    def ready(self):
        from . import signals
