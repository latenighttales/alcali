import pendulum
from django.urls import reverse


def test_dummy_clean(run_sql):
    run_sql("TRUNCATE TABLE `salt_returns`")
    assert True


def test_run(admin_client):
    response = admin_client.get(reverse("run"))
    assert response.status_code == 200


def test_run_get_param(admin_client):
    response = admin_client.get(reverse("run") + "?tgt=master&fun=state.apply")
    assert response.status_code == 200
    assert response.context["get_params"]["fun"][0] == "state.apply"


def test_run_failed_tooltip(admin_client):
    response = admin_client.post(
        reverse("run"), {"tooltip": "foobar", "client": "local"}
    )
    assert response.status_code == 200
    assert response.json() == {}


def test_run_raw(admin_client):
    response = admin_client.post(
        reverse("run"), {"command": "salt '*' cmd.run 'echo foo'"}
    )
    assert response.status_code == 200


def test_run_schedule_recurrent(admin_client):
    response = admin_client.post(
        reverse("run"),
        {
            "minion_list": "*",
            "function_list": "test.ping",
            "client": "local",
            "schedule-sw": "on",
            "schedule_type": "recurrent",
            "cron": "* * * * *",
        },
    )
    assert response.status_code == 200
    assert b"master" in response.content


def test_run_schedule_once(admin_client):
    response = admin_client.post(
        reverse("run"),
        {
            "minion_list": "*",
            "function_list": "test.ping",
            "client": "local",
            "schedule-sw": "on",
            "schedule_type": "once",
            "schedule": pendulum.now().add(days=1).format("YYYY-MM-DD HH:mm"),
        },
    )
    assert response.status_code == 200
    assert b"master" in response.content


def test_runner_raw(admin_client):
    response = admin_client.post(
        reverse("run"), {"command": "salt --client=runner pillar.show_top"}
    )
    assert response.status_code == 200
    assert b"base" in response.content


def test_wheel_raw(admin_client):
    response = admin_client.post(
        reverse("run"), {"command": "salt --client=wheel key.list_all"}
    )
    assert response.status_code == 200
    assert b"master" in response.content


def test_dummy_clean_out(run_sql):
    run_sql("TRUNCATE TABLE `salt_returns`")
    assert True
