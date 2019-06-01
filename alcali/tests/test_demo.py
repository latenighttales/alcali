import pytest
from django.urls import reverse

from alcali.web.models.alcali import Keys, Minions, Functions, Schedule
from alcali.web.models.salt import SaltReturns


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
def test_add_keys(admin_client):
    """
    user_settings are working as expected, and /wheel behave correctly.
    """
    assert Keys.objects.get(minion_id="master").status != "accepted"
    admin_client.get(reverse("index"), follow=True)
    response = admin_client.post(reverse("run"), {"action": "accept", "target": "*"})
    assert response.status_code == 200
    assert hasattr(response, "json")
    resp = response.json()
    assert "master" in resp["return"][0]["data"]["return"]["minions"]
    # TODO: can't make it work!
    # keys = Keys.objects.all()
    # keys._result_cache = None
    # assert len([i for i in Keys.objects.all() if i.status == 'accepted']) == 2


@pytest.mark.django_db()
def test_add_minions(admin_client):
    assert Minions.objects.count() == 0
    response = admin_client.post(reverse("minions"), {"minion": "*"})
    assert response.status_code == 200
    assert Minions.objects.count() > 0


@pytest.mark.django_db()
def test_run_highstate(admin_client):
    for minion in Minions.objects.all():
        assert minion.conformity() is False
    response = admin_client.post(
        reverse("run"),
        {"minion_list": "*", "function_list": "state.apply", "client": "local"},
    )
    assert response.status_code == 200
    assert SaltReturns.objects.filter(fun="state.apply")
    for minion in Minions.objects.all():
        assert minion.conformity() is True


@pytest.mark.django_db()
def test_runner(admin_client):
    response = admin_client.get(reverse("index"), follow=True)
    response = admin_client.post(
        reverse("run"), {"function_list": "jobs.active", "client": "runner"}
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_wheel(admin_client):
    response = admin_client.get(reverse("index"), follow=True)
    response = admin_client.post(
        reverse("run"),
        {"function_list": "key.name_match", "args": "master", "client": "wheel"},
    )
    assert response.status_code == 200
    # assert SaltReturns.objects.filter(fun='key.name_match')


@pytest.mark.django_db()
def test_run_conformity_state(admin_client):
    response = admin_client.post(
        reverse("run"),
        {
            "minion_list": "*",
            "function_list": "grains.item",
            "args": "os",
            "client": "local",
        },
    )
    response = admin_client.post(
        reverse("run"), {"command": "salt * grains.item saltversion"}
    )
    for minion in Minions.objects.all():
        assert minion.custom_conformity("grains.item", "os")
        assert minion.custom_conformity("grains.item", "saltversion")


@pytest.mark.django_db()
def test_refresh_keys(admin_client):
    keys_attr = ["minion_id", "pub", "status"]
    current_keys = list(Keys.objects.filter().values_list(*keys_attr))
    response = admin_client.post(reverse("keys"), {"action": "refresh"})
    assert response.status_code == 200
    updated_keys = list(Keys.objects.filter().values_list(*keys_attr))
    assert current_keys == updated_keys


@pytest.mark.django_db()
def test_init_db(admin_client):
    assert Functions.objects.count() == 0
    response = admin_client.post(
        reverse("settings"), {"action": "init_db", "target": "master"}
    )
    assert response.status_code == 200
    for funct_type in ["local", "runner", "wheel"]:
        assert Functions.objects.filter(type=funct_type).count() > 0
    # Assert tooltips are working.
    response = admin_client.post(
        reverse("run"), {"tooltip": "grains.item", "client": "local"}
    )
    assert response.status_code == 200
    assert (
        response.json()["desc"]
        == Functions.objects.filter(name="grains.item").values_list(
            "description", flat=True
        )[0]
    )

    response = admin_client.post(
        reverse("run"), {"tooltip": "state.event", "client": "runner"}
    )
    assert response.status_code == 200
    assert (
        response.json()["desc"]
        == Functions.objects.filter(name="state.event", type="runner").values_list(
            "description", flat=True
        )[0]
    )

    response = admin_client.post(
        reverse("run"), {"tooltip": "key.list_all", "client": "wheel"}
    )
    assert response.status_code == 200
    assert (
        response.json()["desc"]
        == Functions.objects.filter(name="key.list_all").values_list(
            "description", flat=True
        )[0]
    )


@pytest.mark.django_db()
def test_add_minion_field(admin_client):
    response = admin_client.post(
        reverse("settings"),
        {
            "name": "highstate",
            "function": "state.show_highstate",
            "action": "create_field",
        },
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"
    response = admin_client.post(reverse("minions"), {"minion": "master"})
    assert response.status_code == 200
    assert "refreshed" in response.json()


@pytest.mark.django_db()
def test_change_notifs(admin_client, admin_user):
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
    response = admin_client.post(
        reverse("settings"), {"notifs_created": "on", "action": "notifications"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"


@pytest.mark.django_db()
def test_schedules(admin_client, run_sql):
    assert Schedule.objects.count() == 0
    response = admin_client.post(
        reverse("run"),
        {"command": "salt master schedule.add job1 function='test.ping' seconds=3600"},
    )
    assert response.status_code == 200
    response = admin_client.post("/schedule", {"action": "refresh", "minion": "master"})
    assert response.status_code == 200
    assert len(Schedule.objects.all()) > 0
    run_sql("TRUNCATE TABLE `salt_returns`")
