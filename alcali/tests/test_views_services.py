from django.urls import reverse

from alcali.web.models.alcali import MinionsCustomFields
from ..web.forms import AlcaliUserForm


def test_schedule(admin_client):
    response = admin_client.get(reverse("schedule"))
    assert response.status_code == 200


def test_schedule_list(admin_client, schedule):
    response = admin_client.post(reverse("schedule"), {"strange": "behaviour"})
    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["data"][0]


def test_schedule_refresh(admin_client):
    response = admin_client.post(
        reverse("schedule"), {"action": "refresh", "minion": "master"}
    )
    assert response.status_code == 200
    assert "job1" in response.json()["refreshed"]["master"]


def test_schedule_manage(admin_client, minion_master):
    response = admin_client.post(
        reverse("schedule"),
        {"action": "disable_job", "minion": "master", "name": "job1"},
    )
    assert response.status_code == 200


def test_conformity_add(admin_client, minion_master):
    response = admin_client.post(
        reverse("run"),
        {"minion_list": "*", "function_list": "grains.item", "args": "os"},
    )
    response = admin_client.post(
        reverse("conformity"), {"name": "os", "function": "grains.item os"}
    )
    assert response.status_code == 200
    assert minion_master.custom_conformity("grains.item", "os")
    response = admin_client.get(reverse("index"))
    assert "OS" in response.context["conformity_name"]
    assert response.context["conformity"][1]["Debian"] == 1


def test_settings(admin_client):
    response = admin_client.get(reverse("settings"))
    assert response.status_code == 200


def test_settings_notifs(admin_client):
    response = admin_client.post(
        reverse("settings"), {"action": "notifications", "created": "on"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"


def test_settings_minion_field(admin_client, minion_master):
    response = admin_client.post(
        reverse("settings"), {"name": "highstate", "function": "state.show_highstate"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"
    response = admin_client.post(reverse("minions"), {"minion": "master"})
    assert response.status_code == 200
    assert "refreshed" in response.json()
    assert MinionsCustomFields.objects.count() > 0
    response = admin_client.post(
        reverse("settings"), {"name": "foo", "function": "bar"}
    )
    response = admin_client.post(
        reverse("settings"), {"action": "delete_field", "target": "foo"}
    )
    assert "result" in response.json()


def test_events(admin_client):
    response = admin_client.get(reverse("events"))
    assert response.status_code == 200
    assert b"salt/" in response.content


def test_users(admin_client):
    response = admin_client.get(reverse("users"))
    assert response.status_code == 200


def test_users_list(admin_client):
    response = admin_client.post(reverse("users"), {"action": "list"})
    assert response.status_code == 200
    assert "admin" in response.json()["data"][0]


def test_users_form_create(admin_client):
    form_data = {
        "username": "foo",
        "first_name": "bar",
        "last_name": "baz",
        "email": "foo@example.com",
        "password1": "superstrongpassword",
        "password2": "superstrongpassword",
    }
    form = AlcaliUserForm(data=form_data)
    assert form.is_valid()
