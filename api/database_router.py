from .models import UserSettings

from django_currentuser.middleware import get_current_user


class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    route_db_tables = {"jids", "salt_returns", "salt_events"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.db_table in self.route_db_tables:
            user = get_current_user()
            return UserSettings.objects.get(user=user).settings["selected_master"]
        return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.db_table in self.route_db_tables:
            user = get_current_user()
            return UserSettings.objects.get(user=user).settings["selected_master"]
        return "default"
