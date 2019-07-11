from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


UserModel = get_user_model()


class Command(BaseCommand):
    help = "Create Token for a given user"

    def create_user_token(self, username, reset_token):
        user = UserModel.objects.get(username=username)

        # Just saving the user should be enough.
        if reset_token:
            user.user_settings.generate_token()

        token = UserModel.objects.get(username=username).user_settings.token
        return token

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

        parser.add_argument(
            "-r",
            "--reset",
            action="store_true",
            dest="reset_token",
            default=False,
            help="Reset existing User token and create a new one",
        )

    def handle(self, *args, **options):
        username = options["username"]
        reset_token = options["reset_token"]

        try:
            token = self.create_user_token(username, reset_token)
        except UserModel.DoesNotExist:
            raise CommandError(
                "Cannot create the Token: user {0} does not exist".format(username)
            )
        if options["reset_token"]:
            self.stdout.write(
                "Generated token {0} for user {1}".format(token, username)
            )
        else:
            self.stdout.write("user {1}'s token: {0}".format(token, username))
