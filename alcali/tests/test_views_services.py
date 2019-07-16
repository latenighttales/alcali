from django.contrib.auth.models import User
from django.urls import reverse
import pytest

from alcali.web.models.alcali import MinionsCustomFields, Notifications
from ..web.forms import AlcaliUserForm, AlcaliUserChangeForm


def test_event_stream(admin_client):
    response = admin_client.get(reverse("event_stream"))
    assert response.status_code == 200


def test_search(admin_client, minion_master, dummy_state):
    response = admin_client.get(reverse("search") + "?q=master")
    assert response.status_code == 200
    assert response.context["minions"]
    response = admin_client.get(reverse("search") + "?q=pass_salt")
    assert response.status_code == 200
    assert response.context["jobs"]
    response = admin_client.get(reverse("search"))
    assert response.status_code == 302


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


def test_schedule_add(admin_client, minion_master):
    response = admin_client.post(
        reverse("schedule"), {"cron": "0 0 * * *", "target": "master"}
    )
    assert response.status_code == 200


def test_conformity_highstate_add(admin_client, minion_master):
    response = admin_client.post(
        reverse("schedule"), {"cron": "0 0 * * *", "target": "master"}
    )
    assert response.status_code == 200
    assert "master" in response.json()["result"]


def test_conformity_get(admin_client, minion_master):
    response = admin_client.get(reverse("conformity"))
    assert response.status_code == 200


def test_conformity_list(
    admin_client, minion, highstate, minion_master, highstate_diff
):
    response = admin_client.post(reverse("conformity"), {"action": "list"})
    assert response.status_code == 200
    assert "data" in response.json()
    assert "Minion id" in response.json()["columns"]
    assert response.json()["data"][0][2] is False


def test_conformity_detail_get(
    admin_client, minion, highstate, minion_master, highstate_diff
):
    response = admin_client.post(
        reverse("settings"),
        {"name": "os", "function": "grains.item os", "action": "create_conformity"},
    )
    response = admin_client.get(
        reverse("conformity_detail", kwargs={"minion_id": minion.minion_id})
    )
    assert response.status_code == 200
    assert response.context["minion_id"] == minion.minion_id
    assert "os" in response.context["custom_conformity"][0]
    assert "install_alcali" in response.context["succeeded"]


def test_conformity_add(admin_client, minion_master):
    master = minion_master
    response = admin_client.post(
        reverse("run"),
        {
            "minion_list": "*",
            "function_list": "grains.item",
            "args": "os",
            "client": "local",
        },
    )
    assert response.status_code == 200
    response = admin_client.post(
        reverse("settings"),
        {"name": "os", "function": "grains.item os", "action": "create_conformity"},
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"


def test_conformity_delete(admin_client):
    response = admin_client.post(
        reverse("settings"),
        {"name": "foo", "function": "bar", "action": "create_conformity"},
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"
    response = admin_client.post(
        reverse("settings"), {"action": "delete_conformity", "target": "foo"}
    )
    assert response.status_code == 200
    assert "result" in response.json()


def test_settings(admin_client):
    response = admin_client.get(reverse("settings"))
    assert response.status_code == 200


def test_settings_notifs(admin_client):
    response = admin_client.post(
        reverse("settings"),
        {"action": "notifications", "created": "on", "returned": "on"},
    )
    assert response.status_code == 200
    assert response.json()["result"] == "updated"


def test_settings_minion_field(admin_client, minion_master):
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
    assert MinionsCustomFields.objects.count() > 0
    response = admin_client.post(
        reverse("settings"),
        {"name": "foo", "function": "bar", "action": "create_field"},
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


def test_users_renew(admin_client, admin_user):
    current_token = admin_user.user_settings.token
    response = admin_client.post(reverse("users"), {"action": "renew", "user": "admin"})
    assert response.status_code == 200
    assert response.json()["result"] == "success"
    assert current_token != User.objects.get(username="admin").user_settings.token


def test_users_revoke(admin_client, admin_user):
    response = admin_client.post(
        reverse("users"), {"action": "revoke", "user": "admin"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "success"
    assert User.objects.get(username="admin").user_settings.token == "REVOKED"
    admin_client.post(reverse("users"), {"action": "renew", "user": "admin"})


def test_users_delete(admin_client, dummy_user):
    response = admin_client.post(
        reverse("users"), {"action": "delete", "user": "dummy_user"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "success"
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username="dummy_user")


def test_users_edit(admin_client, dummy_user):
    response = admin_client.post(
        reverse("users"), {"action": "edit", "user": "dummy_user"}
    )
    assert response.status_code == 200
    assert response.context["form"]


def test_users_create(admin_client):
    response = admin_client.post(
        reverse("users"),
        {
            "username": "foobar",
            "first_name": "bar",
            "last_name": "baz",
            "email": "foo@example.com",
        },
    )
    assert response.status_code == 200


def test_users_edit_form(admin_client, admin_user):
    response = admin_client.get(reverse("edit_user", args=[admin_user.id]))
    assert response.status_code == 200
    assert response.context["form"]


def test_users_edit_post(admin_client, dummy_user):
    response = admin_client.post(
        reverse("edit_user", args=[dummy_user.id]),
        {
            "username": "dummy_user",
            "first_name": "dummy",
            "last_name": "user",
            "email": "dummy_user1@example.com",
        },
    )
    assert response.status_code == 200
    assert response.json()["result"] == "success"


def test_notifications(admin_client, admin_user, minion_master):
    response = admin_client.post(
        reverse("run"),
        {"minion_list": "*", "function_list": "test.ping", "client": "local"},
    )
    assert response.status_code == 200
    assert admin_user.notifications


def test_notifications_create(admin_client):
    notif = {
        "type": "returned",
        "tag": "salt/job/20190525145731820194/ret/master",
        "data": '{"fun_args":[],"jid":"20190525145731820194","return":true,'
        '"retcode":0,"success":true,"cmd":"_return",'
        '"_stamp":"2019-05-25T14:57:31.890646","fun":"test.ping",'
        '"id":"master"}',
    }
    ret = {
        "color": "bg-blue-grey",
        "link": "/jobs/20190525145731820194/master",
        "icon": "subdirectory_arrow_left",
        "text": "test.ping returned for master",
    }
    response = admin_client.post(reverse("notifications"), notif)
    assert response.status_code == 200
    for key, val in ret.items():
        assert val in response.context["notif_{}".format(key)]


def test_notifications_delete_one(admin_client, notification):
    notif_id = Notifications.objects.first().id
    response = admin_client.post(
        reverse("notifications"), {"action": "delete", "id": notif_id}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "success"
    with pytest.raises(Notifications.DoesNotExist):
        Notifications.objects.get(id=notif_id)


def test_notifications_delete_all(admin_client, notification):
    response = admin_client.post(
        reverse("notifications"), {"action": "delete", "id": "*"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "success"
    assert Notifications.objects.count() == 0


def test_404(admin_client):
    response = admin_client.get("/foo")
    assert response.status_code == 404
    assert response.context["exception"]


@pytest.mark.django_db
def test_users_form_create():
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


@pytest.mark.django_db
def test_users_form_update():
    form_data = {
        "username": "foobar",
        "first_name": "bar",
        "last_name": "baz",
        "email": "foo@example.com",
    }
    form = AlcaliUserChangeForm(data=form_data)
    assert form.is_valid()
