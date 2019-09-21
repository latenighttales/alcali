import binascii
import json
import os

from django.contrib.auth.models import User
from django.db.models import Q

from django.db import models


class FindJobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(fun="saltutil.find_job")


class Jids(models.Model):
    jid = models.CharField(primary_key=True, db_index=True, max_length=255)
    load = models.TextField()

    def loaded_load(self):
        return json.loads(self.load)

    def user(self):
        if "user" in self.loaded_load():
            return self.loaded_load()["user"]
        return ""

    class Meta:
        managed = False
        db_table = "jids"
        app_label = "api"


class SaltReturns(models.Model):
    fun = models.CharField(max_length=50, db_index=True)
    jid = models.CharField(max_length=255, db_index=True)
    # Field renamed because it was a Python reserved word.
    return_field = models.TextField(db_column="return")
    id = models.CharField(max_length=255, primary_key=True)
    success = models.CharField(max_length=10)
    full_ret = models.TextField()
    alter_time = models.DateTimeField()

    objects = FindJobManager()

    def loaded_ret(self):
        return json.loads(self.full_ret)

    def user(self):
        # TODO: find a better way?
        return Jids.objects.get(jid=self.jid).user()

    def arguments(self):
        ret = self.loaded_ret()
        if "fun_args" in ret and ret["fun_args"]:
            return " ".join(str(i) for i in ret["fun_args"])
        return ""

    def success_bool(self):
        ret = self.loaded_ret()
        if "success" in ret:
            return ret["success"]
        if "return" in ret:
            if "success" in ret["return"]:
                return ret["return"]["success"]
            if "result" in ret["return"]:
                return ret["return"]["result"]
        return self.jid

    class Meta:
        managed = False
        db_table = "salt_returns"
        app_label = "api"


class SaltEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, db_index=True)
    data = models.TextField()
    alter_time = models.DateTimeField()
    master_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "salt_events"
        app_label = "api"


# Alcali custom.
class Functions(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        db_table = "salt_functions"
        app_label = "api"


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
        )
        states = sorted(states, key=lambda x: x.jid, reverse=True)

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
            # Flat out error(return is a string)
            if isinstance(highstate_ret["return"], list):
                return False
            # One of the state is not ok
            if not highstate_ret["return"][state]["result"]:
                return False
        return True

    def custom_conformity(self, fun, *args):

        # First, filter with fun.
        jobs = SaltReturns.objects.filter(fun=fun, id=self.minion_id).order_by(
            "-alter_time"
        )
        if not jobs:
            return False
        if args:
            for job in jobs:
                ret = job.loaded_ret()
                # if provided args are the same.
                if not list(
                    set(args) ^ {i for i in ret["fun_args"] if isinstance(i, str)}
                ):
                    return ret["return"]
        # If no args or kwargs, just return the first job.
        else:
            job = jobs.first()
            return job.loaded_ret()["return"]

    def __str__(self):
        return "{}".format(self.minion_id)

    class Meta:
        db_table = "salt_minions"
        app_label = "api"


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
        app_label = "api"


class MinionsCustomFields(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    minion = models.ForeignKey(
        Minions, related_name="custom_fields", on_delete=models.CASCADE
    )
    function = models.CharField(max_length=255)

    def __str__(self):
        return "{}: {}".format(self.name, self.function)

    class Meta:
        db_table = "minions_custom_fields"
        app_label = "api"


class Schedule(models.Model):
    minion = models.CharField(max_length=128, null=False, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    job = models.TextField()

    def loaded_job(self):
        return json.loads(self.job)

    class Meta:
        app_label = "api"


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
        app_label = "api"

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
        app_label = "api"
