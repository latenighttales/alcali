import pytest
from api.models import SaltReturns, SaltEvents


@pytest.mark.django_db()
def test_salt_returns_list(admin_client, jwt):
    response = admin_client.get("/api/jobs/", **jwt)
    assert len(response.json()) == SaltReturns.objects.count()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_salt_returns_filters(jid, highstate, admin_client, jwt):
    highstate()
    response = admin_client.get("/api/jobs/filters/", **jwt)
    assert "2e220fd40bc5" in response.json()["minions"]
    assert response.status_code == 200


@pytest.mark.django_db()
def test_salt_returns_list_filtered(jid, highstate, admin_client, jwt):
    highstate()
    response = admin_client.get("/api/jobs/?limit=1&target[]=2e220fd40bc5", **jwt)
    assert len(response.json()) <= 1
    assert response.status_code == 200


@pytest.mark.django_db()
def test_salt_returns_job(jid, highstate, admin_client, jwt):
    highstate()
    assert SaltReturns.objects.get(jid="20190429180928455927", id="2e220fd40bc5")
    response = admin_client.get("/api/jobs/20190429180928455927/2e220fd40bc5/", **jwt)
    assert response.json()["jid"] == "20190429180928455927"
    assert response.status_code == 200


@pytest.mark.django_db()
def test_salt_returns_list(admin_client, jwt):
    response = admin_client.get("/api/events/", **jwt)
    assert len(response.json()) <= 200
    assert response.status_code == 200


@pytest.mark.django_db()
def test_salt_returns_job_rendered(jid, highstate, admin_client, jwt):
    highstate()
    assert SaltReturns.objects.get(jid="20190429180928455927", id="2e220fd40bc5")
    response = admin_client.get(
        "/api/jobs/20190429180928455927/2e220fd40bc5/rendered_state/", **jwt
    )
    assert response.status_code == 200
