import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Return Alcali location"

    def handle(self, *args, **options):

        current_path = os.path.dirname(os.path.abspath(__file__))
        current_path = os.path.abspath(os.path.join(current_path, "..", "..", ".."))
        self.stdout.write("{}".format(current_path))
