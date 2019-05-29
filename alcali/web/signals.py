from django.db.models.signals import pre_save, post_save

# from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

# from alcali.web.backend.netapi import set_perms
from .models.alcali import UserSettings, Notifications


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):

    # Create related UserSettings when a new User is created.
    if created:
        UserSettings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):

    # Save UserSettings when user is saved.
    instance.user_settings.save()


@receiver(pre_save, sender=Notifications)
def clean_notifs(sender, instance, **kwargs):

    # Only keep max notifs nb in database.
    max_notifs = instance.user.user_settings.max_notifs
    notif_nb = Notifications.objects.filter(user=instance.user).count()
    if notif_nb > max_notifs:
        ids = Notifications.objects.order_by("-pk").values_list("pk", flat=True)[
            :max_notifs
        ]
        Notifications.objects.exclude(pk__in=list(ids)).delete()


# @receiver(user_logged_in)
# def set_perms_on_login(sender, user, request, **kwargs):
#     set_perms()
