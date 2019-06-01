import time

from django.test import SimpleTestCase
from django.urls import reverse


def test_redirect_anonymous(client):
    response = client.get(reverse("index"), follow=True)
    # TODO: why next?
    SimpleTestCase().assertRedirects(response, "/login/?next=%2F")


def test_index(admin_client):
    response = admin_client.get(reverse("index"))
    assert response.status_code == 200


def test_graph_no_filter(admin_client, highstate, dummy_state):
    highstate()
    response = admin_client.post(reverse("index"), {"period": 0})
    assert response.status_code == 200
    assert response.json()["series"][0][0] == 2


def test_graph_highstate_filter(admin_client, highstate, dummy_state):
    highstate()
    response = admin_client.post(reverse("index"), {"period": 0, "filter": "highstate"})
    assert response.status_code == 200
    assert response.json()["series"][0][0] == 1


def test_graph_other_filter(admin_client, highstate, dummy_state):
    highstate()
    response = admin_client.post(reverse("index"), {"period": 0, "filter": "other"})
    assert response.status_code == 200
    assert response.json()["series"][0][0] == 1


def test_jobs(admin_client):
    response = admin_client.get(reverse("job_list"))
    assert response.status_code == 200


def test_jobs_default(admin_client, jid, highstate, dummy_jid, dummy_state):
    highstate()
    response = admin_client.post(reverse("job_list"), {"limit": 100})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_jobs_filter_user(admin_client, jid, highstate, dummy_jid, dummy_state):
    highstate()
    response = admin_client.post(reverse("job_list"), {"limit": 100, "user": "admin"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert "state.apply" in response.json()["data"][0]


def test_jobs_filter_minion(admin_client, jid, highstate, dummy_jid, dummy_state):
    highstate()
    response = admin_client.post(
        reverse("job_list"), {"limit": 100, "minion": "master"}
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert "alcali.pass_salt" in response.json()["data"][0]


def test_jobs_filter_date(admin_client, jid, highstate, dummy_jid, dummy_state):
    highstate()
    today = date = time.strftime("%Y-%m-%d")
    response = admin_client.post(
        reverse("job_list"),
        {"limit": 100, "minion": "master", "date": ["{}".format(today)]},
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert "alcali.pass_salt" in response.json()["data"][0]


def test_job_details(admin_client, jid, highstate):
    highstate()
    response = admin_client.get(
        reverse(
            "job_detail",
            kwargs={"jid": "20190429180928455927", "minion_id": "2e220fd40bc5"},
        )
    )
    assert response.status_code == 200


def test_minion_delete(admin_client, minion):
    response = admin_client.post(
        reverse("minions"), {"minion": "2e220fd40bc5", "action": "delete"}
    )
    assert response.status_code == 200
    assert response.json()["2e220fd40bc5"] == "deleted"


def test_minion_list(admin_client, highstate, minion_master, dummy_state):
    highstate(minion="master")
    # TODO: if no params are passed, no response.json?
    response = admin_client.post(reverse("minions"), {"strange": "behaviour"})
    assert response.status_code == 200
    assert "master" in response.json()["data"][0]


def test_minion_refresh(admin_client, minion, key):
    response = admin_client.post(
        reverse("minions"), {"minion": "*", "action": "refresh"}
    )
    assert response.status_code == 200
    assert response.json()["refreshed"][0]


def test_minion_detail(admin_client, minion_master):
    response = admin_client.get(
        reverse("minion_detail", kwargs={"minion_id": "master"})
    )
    assert response.status_code == 200


def test_minion_detail_graph(admin_client, highstate, dummy_state, minion_master):
    highstate()
    response = admin_client.post(
        reverse("minion_detail", kwargs={"minion_id": "master"}), {"period": 0}
    )
    assert response.status_code == 200
    # Already filtered for this minion.
    assert response.json()["series"][0][0] > 0


def test_keys(admin_client):
    response = admin_client.get(reverse("keys"))
    assert response.status_code == 200


def test_key_list(admin_client, key):
    # TODO find out why!
    response = admin_client.post(reverse("keys"), {"strange": "behaviour"})
    assert response.status_code == 200
    assert len(response.json()["data"][0]) > 0


def test_key_refresh(admin_client, key):
    response = admin_client.post(reverse("keys"), {"action": "refresh"})
    assert response.status_code == 200
    assert response.json()["refreshed"]


def test_events(admin_client):
    response = admin_client.get(reverse("events"))
    assert response.status_code == 200
