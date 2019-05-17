from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from alcali.web.models.alcali import UserSettings

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Create Token for a given user'

    def create_user_token(self, username, reset_token):
        user = UserModel.objects.get(username=username)

        # TODO: re implement
        if reset_token:
            pass

        token = UserModel.objects.get(username=username).token
        return token

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

        parser.add_argument(
            '-r',
            '--reset',
            action='store_true',
            dest='reset_token',
            default=False,
            help='Reset existing User token and create a new one',
        )

    def handle(self, *args, **options):
        username = options['username']
        reset_token = options['reset_token']

        try:
            token = self.create_user_token(username, reset_token)
        except UserModel.DoesNotExist:
            raise CommandError(
                'Cannot create the Token: user {0} does not exist'.format(
                    username)
            )
        self.stdout.write(
            'Generated token {0} for user {1}'.format(token.key, username))
