import binascii
import json
import os

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
        return '{}'.format(self.name)

    class Meta:
        db_table = 'salt_functions'
        app_label = 'web'


class Minions(models.Model):
    minion_id = models.CharField(max_length=128, null=False, blank=False)
    grain = models.TextField()
    pillar = models.TextField()

    def loaded_grain(self):
        return json.loads(self.grain)

    def loaded_pillar(self):
        return json.loads(self.pillar)

    def last_job(self):
        return SaltReturns.objects.filter(
            id=self.minion_id
        ).order_by('-alter_time').first()

    def last_highstate(self):
        return SaltReturns.objects.filter(
            Q(fun='state.apply') | Q(fun='state.highstate'), id=self.minion_id
        ).order_by('-alter_time').first()

    def conformity(self):
        last_highstate = self.last_highstate()
        if not last_highstate:
            return False
        highstate_ret = last_highstate.loaded_ret()
        for state in highstate_ret['return']:
            if not highstate_ret['return'][state]['result']:
                return False
        return True

    def custom_conformity(self, fun, *args, **kwargs):
        jobs = SaltReturns.objects.filter(fun=fun,
                                          id=self.minion_id).order_by('-alter_time')
        # TODO: kwargs...
        if args or kwargs:
            for job in jobs:
                ret = job.loaded_ret()
                # if provided args are the same.
                if not list(set(args) ^ set(
                        [i for i in ret['fun_args'] if isinstance(i, str)])):
                    return ret['return']
        else:
            return [job.loaded_ret()['return'] for job in jobs.first()]

    def __str__(self):
        return '{}'.format(self.minion_id)

    class Meta:
        db_table = 'salt_minions'
        app_label = 'web'


class Keys(models.Model):
    KEY_STATUS = (
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('denied', 'denied'),
        ('unaccepted', 'unaccepted'),
    )
    minion_id = models.CharField(max_length=255)
    pub = models.TextField(blank=True)
    status = models.CharField(max_length=64, choices=KEY_STATUS)

    def __str__(self):
        return '{}'.format(self.minion_id)

    class Meta:
        # TODO add constraints (only one accepted per minion_id)
        db_table = 'salt_keys'
        app_label = 'web'


class MinionsCustomFields(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    minion = models.ForeignKey(Minions, on_delete=models.CASCADE)
    function = models.CharField(max_length=255)

    def __str__(self):
        return '{}: {}'.format(self.name, self.function)

    class Meta:
        db_table = 'minions_custom_fields'
        app_label = 'web'


class Schedule(models.Model):
    minion = models.CharField(max_length=128, null=False, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    job = models.TextField()

    def loaded_job(self):
        return json.loads(self.job)

    class Meta:
        app_label = 'web'


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class UserSettings(models.Model):
    """
    The default authorization token model.
    """
    user = models.OneToOneField(User,
                                primary_key=True,
                                related_name='user_settings',
                                on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    notifs_created = models.BooleanField(default=False)
    notifs_published = models.BooleanField(default=False)
    notifs_returned = models.BooleanField(default=True)
    notifs_event = models.BooleanField(default=False)
    salt_permissions = models.TextField()

    def wheel(self):
        try:
            for perm in json.loads(self.salt_permissions):
                if ('@wheel' in perm) or ('wheel' in perm):
                    return True
        except json.decoder.JSONDecodeError:
            return False
        return False

    def runner(self):
        try:
            for perm in json.loads(self.salt_permissions):
                if ('@runner' in perm) or ('runner' in perm):
                    return True
        except json.decoder.JSONDecodeError:
            return False
        return False

    class Meta:
        db_table = 'user_settings'
        app_label = 'web'

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
        db_table = 'conformity'
        app_label = 'web'
