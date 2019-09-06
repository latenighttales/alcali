import os
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Check access to database and that env var are set"

    def handle(self, *args, **options):

        unset = []
        for env in [
            "MASTER_MINION_ID",
            "DB_BACKEND",
            "DB_NAME",
            "DB_USER",
            "DB_PASS",
            "DB_HOST",
            "DB_PORT",
            "SECRET_KEY",
            "ALLOWED_HOSTS",
            "SALT_URL",
            "SALT_AUTH",
        ]:
            try:
                os.environ[env]
            except KeyError:
                unset.append(env)

        db_conn = connections["default"]
        try:
            db_conn.cursor()
        except OperationalError as e:
            error = e
        else:
            error = None

        self.stdout.write("db:\t{}\nenv:\t{}".format(error or "ok", unset or "ok"))
