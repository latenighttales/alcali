from api.models import Conformity, Device, DeviceGroup, Functions, JobTemplate, Keys, Minions, MinionsCustomFields, SaltEvents, Schedule, UserSettings
from django.contrib import admin

admin.site.register(Minions)
admin.site.register(Keys)
admin.site.register(MinionsCustomFields)
admin.site.register(Schedule)
admin.site.register(Functions)
# admin.site.register(Users)
admin.site.register(UserSettings)
admin.site.register(Conformity)
admin.site.register(SaltEvents)
admin.site.register(JobTemplate)
admin.site.register(Device)
admin.site.register(DeviceGroup)