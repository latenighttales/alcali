import pytest
from django.urls import reverse

from api.models import Keys, Minions, Functions, Schedule, SaltReturns


def test_demo_default_admin(admin_client):
    """
    Make sure dummy user is available.
    """
    response = admin_client.get(reverse("index"), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_default_perms(client, admin_user):
    """
    Default permissions are added to salt, and stored in user_settings.
    """
    # Set perms.
    username = "admin"
    password = "password"
    client.login(username=username, password=password)
    client.get(reverse("index"), follow=True)
    assert hasattr(admin_user.user_settings, "salt_permissions")


@pytest.mark.django_db()
def test_add_keys(admin_client, jwt):
    """
    user_settings are working as expected, and /wheel behave correctly.
    """
    res = admin_client.post(
        "/api/token/", data={"username": "admin", "password": "password"}
    )
    token = res.data["access"]
    # assert Keys.objects.get(minion_id="master").status != "accepted"
    response = admin_client.post(
        "/api/keys/manage_keys/", {"action": "accept", "target": "*"}, **jwt
    )
    assert response.status_code == 200
    assert hasattr(response, "json")
    resp = response.json()
    assert resp == {"result": "accept on *: done"}


@pytest.mark.django_db()
def test_add_minions(admin_client, jwt):
    assert Minions.objects.count() == 0
    response = admin_client.post("/api/minions/refresh_minions/", **jwt)
    assert response.status_code == 200
    assert Minions.objects.count() > 0


@pytest.mark.django_db()
def test_run_highstate(admin_client, jwt):
    for minion in Minions.objects.all():
        assert minion.conformity() is False
    response = admin_client.post(
        "/api/run/",
        {"target": "*", "function": "state.apply", "client": "local"},
        **jwt
    )
    assert response.status_code == 200
    assert SaltReturns.objects.filter(fun="state.apply")
    for minion in Minions.objects.all():
        assert minion.conformity() is True


@pytest.mark.django_db()
def test_runner(admin_client, jwt):
    response = admin_client.post(
        "/api/run/", {"function": "jobs.active", "client": "runner"}, **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_wheel(admin_client, jwt):
    response = admin_client.post(
        "/api/run/",
        {"function": "key.name_match", "args": "master", "client": "wheel"},
        **jwt
    )
    assert response.status_code == 200
    # assert SaltReturns.objects.filter(fun='key.name_match')


@pytest.mark.django_db()
def test_run_conformity_state(admin_client, jwt):
    response = admin_client.post(
        "/api/run/",
        {"target": "*", "function": "grains.item", "args": "os", "client": "local"},
        **jwt
    )
    response = admin_client.post(
        "/api/run/", {"command": "salt * grains.item saltversion", "raw": True}, **jwt
    )
    for minion in Minions.objects.all():
        assert minion.custom_conformity("grains.item", "os")
        assert minion.custom_conformity("grains.item", "saltversion")


@pytest.mark.django_db()
def test_refresh_keys(admin_client, jwt):
    keys_attr = ["minion_id", "pub", "status"]
    current_keys = list(Keys.objects.filter().values_list(*keys_attr))
    response = admin_client.post("/api/keys/refresh/", {}, **jwt)
    assert response.status_code == 200
    updated_keys = list(Keys.objects.filter().values_list(*keys_attr))
    assert current_keys == updated_keys


@pytest.mark.django_db()
def test_init_db(admin_client, jwt):
    assert Functions.objects.count() == 0
    response = admin_client.post("/api/settings/initdb", {"target": "master"}, **jwt)
    assert response.status_code == 200
    for funct_type in ["local", "runner", "wheel"]:
        assert Functions.objects.filter(type=funct_type).count() > 0
    # # Assert tooltips are working.
    # response = admin_client.post(
    #     reverse("run"), {"tooltip": "grains.item", "client": "local"}
    # )
    # assert response.status_code == 200
    # assert (
    #     response.json()["desc"]
    #     == Functions.objects.filter(name="grains.item").values_list(
    #         "description", flat=True
    #     )[0]
    # )
    #
    # response = admin_client.post(
    #     reverse("run"), {"tooltip": "state.event", "client": "runner"}
    # )
    # assert response.status_code == 200
    # assert (
    #     response.json()["desc"]
    #     == Functions.objects.filter(name="state.event", type="runner").values_list(
    #         "description", flat=True
    #     )[0]
    # )
    #
    # response = admin_client.post(
    #     reverse("run"), {"tooltip": "key.list_all", "client": "wheel"}
    # )
    # assert response.status_code == 200
    # assert (
    #     response.json()["desc"]
    #     == Functions.objects.filter(name="key.list_all").values_list(
    #         "description", flat=True
    #     )[0]
    # )
    #
    #


@pytest.mark.django_db()
def test_add_minion_field(admin_client, jwt):
    response = admin_client.post(
        "/api/minionsfields/",
        {"name": "highstate", "function": "state.show_highstate", "value": "{}"},
        **jwt
    )
    assert response.status_code == 201


@pytest.mark.django_db()
def test_change_notifs(admin_client, admin_user, jwt):
    """
    Default permissions are added to salt, and stored in user_settings.
    """
    notifs_defaults = {
        "notifs_created": False,
        "notifs_published": False,
        "notifs_returned": True,
        "notifs_event": False,
    }
    for status, value in notifs_defaults.items():
        assert getattr(admin_user.user_settings, status) == value
    response = admin_client.patch(
        "/api/userssettings/{}/".format(admin_user.id),
        {"notifs_created": "true"},
        content_type="application/json",
        **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_schedules(admin_client, run_sql, jwt):
    assert Schedule.objects.count() == 0
    response = admin_client.post(
        "/api/run/",
        {
            "command": "salt master schedule.add job1 function='test.ping' seconds=3600",
            "raw": True,
        },
        **jwt
    )
    assert response.status_code == 200
    response = admin_client.post("/api/schedules/refresh/", {}, **jwt)
    assert response.status_code == 200
    assert len(Schedule.objects.all()) > 0
    run_sql("TRUNCATE TABLE `salt_returns`")
