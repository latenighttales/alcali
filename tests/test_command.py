import os
from io import StringIO

import pytest
from django.core.management import call_command, CommandError
from django.conf import settings


@pytest.mark.django_db
def test_check():
    out = StringIO()
    call_command("check", stdout=out)
    assert "db:\tok" in out.getvalue()
    assert "env:\tok" in out.getvalue()


@pytest.mark.django_db
def test_check_env_fail():
    out = StringIO()
    salt_url = os.environ["SALT_URL"]
    del os.environ["SALT_URL"]
    call_command("check", stdout=out)
    assert "db:\tok" in out.getvalue()
    assert "SALT_URL" in out.getvalue()
    os.environ["SALT_URL"] = str(salt_url)


@pytest.mark.django_db
def test_manage_token(admin_user):
    current_token = admin_user.user_settings.token
    out = StringIO()
    call_command("manage_token", "admin", stdout=out)
    assert current_token in out.getvalue()


@pytest.mark.django_db
def test_manage_token_raises():
    out = StringIO()
    with pytest.raises(CommandError) as err:
        call_command("manage_token", "foo", stdout=out)
    assert "user foo does" in str(err.value)


@pytest.mark.django_db
def test_manage_token_reset(admin_user):
    current_token = admin_user.user_settings.token
    out = StringIO()
    call_command("manage_token", "admin", "-r", stdout=out)
    assert current_token not in out.getvalue()


def test_current_version():
    out = StringIO()
    call_command("current_version", stdout=out)
    assert "alcali version {}".format(settings.VERSION) in out.getvalue()


def test_location():
    out = StringIO()
    call_command("location", stdout=out)
    assert "/opt/alcali/code" in out.getvalue()
