import json

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
        app_label = "web"
        managed = False
        db_table = "jids"


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
        app_label = "web"
        managed = False
        db_table = "salt_returns"


class SaltEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, db_index=True)
    data = models.TextField()
    alter_time = models.DateTimeField()
    master_id = models.CharField(max_length=255)

    def loaded_data(self):
        return json.loads(self.data)

    class Meta:
        app_label = "web"
        managed = False
        db_table = "salt_events"
