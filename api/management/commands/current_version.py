from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Return Alcali version"

    def handle(self, *args, **options):

        version = settings.VERSION
        self.stdout.write("alcali version {}".format(version))
