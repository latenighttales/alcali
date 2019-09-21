import datetime

import pytest
from django.urls import reverse

from api.models import (
    Keys,
    Minions,
    SaltReturns,
    MinionsCustomFields,
    Schedule,
    UserSettings,
)


@pytest.mark.django_db()
def test_index(admin_client):
    response = admin_client.get(reverse("index"))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_keys_list(key, admin_client, jwt):
    response = admin_client.get("/api/keys/", **jwt)
    assert len(response.json()) == Keys.objects.count()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_keys_refresh(key, admin_client, jwt):
    response = admin_client.post("/api/keys/refresh/", {}, **jwt)
    assert response.json()["result"] == "refreshed"
    assert response.status_code == 200


@pytest.mark.django_db()
def test_keys_status(key, admin_client, jwt):
    response = admin_client.get("/api/keys/keys_status/", **jwt)
    assert "accepted" in response.json()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_keys_manage(key, admin_client, jwt):
    response = admin_client.post(
        "/api/keys/manage_keys/", {"target": "master", "action": "reject"}, **jwt
    )
    assert "result" in response.json()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_list(minion, admin_client, jwt):
    response = admin_client.get("/api/minions/", **jwt)
    assert response.json()[0]["minion_id"] == "2e220fd40bc5"
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_delete(minion, admin_client, jwt):
    response = admin_client.delete("/api/minions/{}/".format(minion.minion_id), **jwt)
    assert response.status_code == 204


@pytest.mark.django_db()
def test_minions_refresh(minion, admin_client, jwt):
    response = admin_client.post(
        "/api/minions/refresh_minions/", {"minion_id": minion.minion_id}, **jwt
    )
    assert "result" in response.json()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_conformity(minion, admin_client, jwt):
    response = admin_client.get("/api/minions/conformity/", **jwt)
    assert "HIGHSTATE" in response.json()["name"]
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_conformity_change(minion, highstate_diff, admin_client, jwt):
    response = admin_client.get("/api/minions/conformity/", **jwt)
    assert "HIGHSTATE" in response.json()["name"]
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_conformity_detail(minion, highstate, admin_client, jwt):
    highstate()
    response = admin_client.get(
        "/api/minions/{}/conformity_detail/".format(minion.minion_id), **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_conformity_detail_highstate(minion, highstate_diff, admin_client, jwt):
    response = admin_client.get(
        "/api/minions/{}/conformity_detail/".format(minion.minion_id), **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_conformity_detail_empty(minion_master, admin_client, jwt):
    response = admin_client.get(
        "/api/minions/{}/conformity_detail/".format(minion_master.minion_id), **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minions_conformity_render(minion, highstate, minion_master, admin_client, jwt):
    highstate()
    response = admin_client.get("/api/conformity/render/", **jwt)
    assert "name" in response.json()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_minion_field_delete(admin_client, jwt):
    response = admin_client.post(
        "/api/minionsfields/",
        {"name": "highstate", "function": "state.show_highstate", "value": "{}"},
        **jwt
    )
    assert response.status_code == 201

    response = admin_client.post(
        "/api/minionsfields/delete_field/", {"name": "highstate"}, **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_schedules_list(schedule, admin_client, jwt):
    response = admin_client.get("/api/schedules/", **jwt)
    assert response.json()[0]["minion"] == "master"
    assert response.json()[0]["name"] == "job2"
    assert response.status_code == 200


@pytest.mark.django_db()
def test_schedules_refresh(admin_client, jwt):
    response = admin_client.post("/api/schedules/refresh/", {}, **jwt)
    assert "result" in response.json()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_schedules_manage(admin_client, jwt):
    response = admin_client.post(
        "/api/run/",
        {
            "command": "salt master schedule.add job2 function='test.ping' seconds=3600",
            "raw": True,
        },
        **jwt
    )
    assert response.status_code == 200
    response = admin_client.post("/api/schedules/refresh/", {}, **jwt)
    assert response.status_code == 200
    response = admin_client.post(
        "/api/schedules/manage/",
        {"action": "delete", "name": "job2", "minion": "master"},
        **jwt
    )
    assert "result" in response.json()
    assert response.status_code == 200


def test_users_list(admin_client, admin_user, jwt):
    response = admin_client.get("/api/users/", **jwt)
    assert response.json()[0]["id"] == admin_user.id
    assert response.status_code == 200


def test_users_refresh_token(admin_client, admin_user, jwt):
    current_token = admin_user.user_settings.token
    response = admin_client.post(
        "/api/users/{}/manage_token/".format(admin_user.id), {"action": "renew"}, **jwt
    )
    assert response.status_code == 200
    assert UserSettings.objects.get(user=admin_user).token != current_token


def test_users_revoke_token(admin_client, admin_user, jwt):
    response = admin_client.post(
        "/api/users/{}/manage_token/".format(admin_user.id), {"action": "revoke"}, **jwt
    )
    assert response.status_code == 200
    assert UserSettings.objects.get(user=admin_user).token == "REVOKED"


def test_jobs_graph(admin_client, jwt):
    response = admin_client.get("/api/jobs/graph?period=2", **jwt)
    assert "labels" in response.json()
    assert response.status_code == 200


def test_jobs_graph_highstate(admin_client, jwt):
    response = admin_client.get("/api/jobs/graph?period=2&fun=highstate", **jwt)
    assert "labels" in response.json()
    assert response.status_code == 200


def test_graph_other_filter(admin_client, highstate, dummy_state, jwt):
    highstate()
    response = admin_client.get("/api/jobs/graph?period=0&fun=other", **jwt)
    assert response.status_code == 200
    assert response.json()["series"][0][0] > 1


def test_stats(admin_client, jwt):
    response = admin_client.get("/api/stats/", **jwt)
    for i in ["jobs", "events", "schedules"]:
        assert i in response.json()
    assert response.status_code == 200


def test_get_events(admin_client):
    response = admin_client.get("/api/event_stream/")
    assert response.status_code == 200


@pytest.mark.django_db()
def test_run_scheduled_cron(admin_client, jwt):
    response = admin_client.post(
        "/api/run/",
        {
            "raw": "true",
            "command": "salt * test.ping",
            "schedule": "true",
            "schedule_type": "cron",
            "cron": "* * * * *",
        },
        **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_run_scheduled_once(admin_client, jwt):
    response = admin_client.post(
        "/api/run/",
        {
            "raw": "true",
            "command": "salt * test.ping",
            "schedule": "{}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            "schedule_type": "once",
        },
        **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_get_functions(admin_client, jwt):
    response = admin_client.get("/api/functions/", **jwt)
    assert response.status_code == 200


@pytest.mark.django_db()
def test_wheel_raw(admin_client, jwt):
    response = admin_client.post(
        "/api/run/",
        {"command": "salt --client=runner pillar.show_top", "raw": True},
        **jwt
    )
    assert response.status_code == 200


@pytest.mark.django_db()
def test_search_minion(admin_client, dummy_state, minion_master, jwt):
    response = admin_client.get("/api/search/?q=master", **jwt)
    assert response.json()["query"] == "master"
    assert response.json()["minions"][0]["minion_id"] == "master"


@pytest.mark.django_db()
def test_search_job(admin_client, dummy_state, dummy_jid, minion_master, jwt):
    response = admin_client.get("/api/search/?q=20190507190955945844", **jwt)
    assert response.json()["query"] == "20190507190955945844"
    assert response.json()["jobs"][0]["jid"] == dummy_state.jid
