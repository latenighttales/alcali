import os

import MySQLdb
from django.conf import settings
from django.db import connections
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test.client import Client

from .fixtures import *


@pytest.fixture()
def run_sql():
    def _run_sql(sql):
        conn = MySQLdb.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            passwd=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"],
            port=int(os.environ["DB_PORT"]),
            ssl={},
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    return _run_sql


# noinspection SqlNoDataSourceInspection
@pytest.yield_fixture(scope="session", autouse=True)
def django_db_setup(django_db_blocker):
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ["DB_HOST"],
        "NAME": os.environ["DB_NAME"],
        "PORT": int(os.environ["DB_PORT"]),
    }
    settings.USE_TZ = False


# # noinspection SqlNoDataSourceInspection
# @pytest.yield_fixture(scope="session", autouse=True)
# def django_db_setup(django_db_blocker):
#     settings.DATABASES["default"] = {
#         "ENGINE": "django.db.backends.mysql",
#         "HOST": os.environ["DB_HOST"],
#         "NAME": os.environ["DB_NAME"],
#         "PORT": int(os.environ["DB_PORT"]),
#     }
#     settings.USE_TZ = False
#
#     yield
#
#     for connection in connections.all():
#         connection.close()
#
#     conn = MySQLdb.connect(
#         host=os.environ["DB_HOST"],
#         user=os.environ["DB_USER"],
#         passwd=os.environ["DB_PASS"],
#         db=os.environ["DB_NAME"],
#         port=int(os.environ["DB_PORT"]),
#         ssl={},
#     )
#     cursor = conn.cursor()
#     cursor.execute("DROP DATABASE IF EXISTS  `salt`")
#     cursor.execute("CREATE DATABASE `salt`")
#     cursor.execute("USE `salt`")
#     cursor.execute(
#         """CREATE TABLE `jids` (
#                         `jid` varchar(255) NOT NULL,
#                         `load` mediumtext NOT NULL,
#                         UNIQUE KEY `jid` (`jid`)
#                       ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
#     )
#
#     cursor.execute(
#         """CREATE TABLE `salt_returns` (
#                         `fun` varchar(50) NOT NULL,
#                         `jid` varchar(255) NOT NULL,
#                         `return` mediumtext NOT NULL,
#                         `id` varchar(255) NOT NULL,
#                         `success` varchar(10) NOT NULL,
#                         `full_ret` mediumtext NOT NULL,
#                         `alter_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                         KEY `id` (`id`),
#                         KEY `jid` (`jid`),
#                         KEY `fun` (`fun`)
#                       ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
#     )
#
#     cursor.execute(
#         """CREATE TABLE `salt_events` (
#                         `id` BIGINT NOT NULL AUTO_INCREMENT,
#                         `tag` varchar(255) NOT NULL,
#                         `data` mediumtext NOT NULL,
#                         `alter_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                         `master_id` varchar(255) NOT NULL,
#                         PRIMARY KEY (`id`),
#                         KEY `tag` (`tag`)
#                       ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
#     )
#     conn.commit()
#
#     with django_db_blocker.unblock():
#         call_command("migrate", verbosity=0, interactive=False)
#         User.objects.filter(username="admin").count() or User.objects.create_superuser(
#             "admin", "admin@example.com", "password"
#         )
#         client = Client()
#         username = "admin"
#         password = "password"
#         client.post("/api/token/", {"username": username, "password": password})
#         client.get("/", follow=True)
#         client.post("/run", {"action": "reject", "target": "*"})
