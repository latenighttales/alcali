from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Return Alcali version"

    def handle(self, *args, **options):

        # TODO: Dynamic
        self.stdout.write("alcali version 2019.2.2")
