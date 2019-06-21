import binascii
import json
import os

import pendulum
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from .salt import SaltReturns


# Alcali custom.
class Functions(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        db_table = "salt_functions"
        app_label = "web"


class Minions(models.Model):
    minion_id = models.CharField(max_length=128, null=False, blank=False)
    grain = models.TextField()
    pillar = models.TextField()

    def loaded_grain(self):
        return json.loads(self.grain)

    def loaded_pillar(self):
        return json.loads(self.pillar)

    def last_job(self):
        return (
            SaltReturns.objects.filter(id=self.minion_id)
            .order_by("-alter_time")
            .first()
        )

    def last_highstate(self):
        # Get all potential jobs.
        states = SaltReturns.objects.filter(
            Q(fun="state.apply") | Q(fun="state.highstate"), id=self.minion_id
        ).order_by("-alter_time")

        # Remove jobs with arguments.
        for state in states:
            if (
                not state.loaded_ret()["fun_args"]
                or state.loaded_ret()["fun_args"][0] == {"test": True}
                or state.loaded_ret()["fun_args"][0] == "test=True"
            ):
                return state
            return None

    def conformity(self):
        last_highstate = self.last_highstate()
        if not last_highstate:
            return None
        highstate_ret = last_highstate.loaded_ret()
        for state in highstate_ret["return"]:
            if not highstate_ret["return"][state]["result"]:
                return False
        return True

    def custom_conformity(self, fun, *args, **kwargs):

        # First, filter with fun.
        jobs = SaltReturns.objects.filter(fun=fun, id=self.minion_id).order_by(
            "-alter_time"
        )
        # TODO: kwargs...
        if args or kwargs:
            for job in jobs:
                ret = job.loaded_ret()
                # if provided args are the same.
                if not list(
                    set(args) ^ {i for i in ret["fun_args"] if isinstance(i, str)}
                ):
                    return ret["return"]
        # If no args or kwargs, just return the first job.
        else:
            return [job.loaded_ret()["return"] for job in jobs.first()]

    def __str__(self):
        return "{}".format(self.minion_id)

    class Meta:
        db_table = "salt_minions"
        app_label = "web"


class Keys(models.Model):
    KEY_STATUS = (
        ("accepted", "accepted"),
        ("rejected", "rejected"),
        ("denied", "denied"),
        ("unaccepted", "unaccepted"),
    )
    minion_id = models.CharField(max_length=255)
    pub = models.TextField(blank=True)
    status = models.CharField(max_length=64, choices=KEY_STATUS)

    def __str__(self):
        return "{}".format(self.minion_id)

    class Meta:
        # TODO add constraints (only one accepted per minion_id)
        db_table = "salt_keys"
        app_label = "web"


class MinionsCustomFields(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    minion = models.ForeignKey(Minions, on_delete=models.CASCADE)
    function = models.CharField(max_length=255)

    def __str__(self):
        return "{}: {}".format(self.name, self.function)

    class Meta:
        db_table = "minions_custom_fields"
        app_label = "web"


class Schedule(models.Model):
    minion = models.CharField(max_length=128, null=False, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    job = models.TextField()

    def loaded_job(self):
        return json.loads(self.job)

    class Meta:
        app_label = "web"


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class UserSettings(models.Model):
    """
    The default authorization token model.
    """

    user = models.OneToOneField(
        User, primary_key=True, related_name="user_settings", on_delete=models.CASCADE
    )
    token = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    max_notifs = models.PositiveIntegerField(default=10)
    notifs_created = models.BooleanField(default=False)
    notifs_published = models.BooleanField(default=False)
    notifs_returned = models.BooleanField(default=True)
    notifs_event = models.BooleanField(default=False)
    salt_permissions = models.TextField()

    def generate_token(self):
        self.token = generate_key()
        self.save()

    class Meta:
        db_table = "user_settings"
        app_label = "web"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_key()
        return super(UserSettings, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Conformity(models.Model):
    name = models.CharField(max_length=255)
    function = models.CharField(max_length=255)

    class Meta:
        db_table = "conformity"
        app_label = "web"


class Notifications(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    notif_type = models.CharField(max_length=32)
    tag = models.CharField(max_length=255)
    data = models.TextField()

    def loaded_data(self):
        return json.loads(self.data)

    def jid(self):
        return self.loaded_data().get("jid")

    def fun(self):
        return self.loaded_data().get("fun")

    def minions(self):
        return self.loaded_data().get("minions")

    def minion_id(self):
        return self.loaded_data().get("id")

    def datetime(self):
        return pendulum.parse(self.loaded_data().get("_stamp"))

    def notif_attr(self):
        notif_attr = {
            "created": {
                "color": "bg-green",
                "link": "#",
                "icon": "add",
                "text": "New Job Created",
            },
            "event": {
                "color": "bg-amber",
                "link": "#",
                "icon": "more_horiz",
                "text": "Job Event",
            },
            "published": {
                "color": "bg-blue",
                "link": "#",
                "icon": "publish",
                "text": "{} published for {} minion(s)".format(
                    self.fun(), len(self.minions()) if self.minions() else 0
                ),
            },
            "returned": {
                "color": "bg-blue-grey",
                "link": "/jobs/{}/{}".format(self.jid(), self.minion_id()),
                "icon": "subdirectory_arrow_left",
                "text": "{} returned for {}".format(self.fun(), self.minion_id()),
            },
        }
        return notif_attr[str(self.notif_type)]

    class Meta:
        db_table = "notifications"
        app_label = "web"
