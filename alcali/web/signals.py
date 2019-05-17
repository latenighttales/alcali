from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models.alcali import UserSettings


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    instance.user_settings.save()
