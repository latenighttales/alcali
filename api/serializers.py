from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    SaltReturns,
    SaltEvents,
    Keys,
    Minions,
    MinionsCustomFields,
    Conformity,
    UserSettings,
    Functions,
    Schedule,
)


class SaltReturnsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    arguments = serializers.CharField()
    success = serializers.BooleanField(source="success_bool")

    class Meta:
        model = SaltReturns
        fields = "__all__"


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaltEvents
        fields = "__all__"


class KeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keys
        fields = "__all__"


class MinionsCustomFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinionsCustomFields
        fields = ("name", "function", "value")


class FunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Functions
        fields = "__all__"


class MinionsSerializer(serializers.ModelSerializer):
    last_job = serializers.DateTimeField(source="last_job.alter_time", default=None)
    last_highstate = serializers.DateTimeField(
        source="last_highstate.alter_time", default=None
    )
    conformity = serializers.BooleanField()
    custom_fields = MinionsCustomFieldsSerializer(many=True, read_only=True)

    class Meta:
        model = Minions
        fields = "__all__"


class ConformitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Conformity
        fields = "__all__"


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    user_settings = UserSettingsSerializer(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        for param in ["is_active", "groups", "user_permissions"]:
            del validated_data[param]
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # Add extra responses here
        data["username"] = self.user.username
        data["id"] = self.user.id
        data["email"] = self.user.email
        return data
