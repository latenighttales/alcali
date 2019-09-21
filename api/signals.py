from django.db.models.signals import pre_save, post_save

from django.dispatch import receiver
from django.contrib.auth.models import User

from api.models import UserSettings


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):

    # Create related UserSettings when a new User is created.
    if created:
        UserSettings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):

    # Save UserSettings when user is saved.
    instance.user_settings.save()
