from django.urls import reverse


def test_dummy_clean(run_sql):
    run_sql("TRUNCATE TABLE `salt_returns`")
    assert True is True


def test_run(admin_client):
    response = admin_client.get(reverse("run"))
    assert response.status_code == 200


def test_run_get_param(admin_client):
    response = admin_client.get(reverse("run") + "?tgt=master&fun=state.apply")
    assert response.status_code == 200
    assert response.context["get_params"]["fun"][0] == "state.apply"


def test_run_failed_tooltip(admin_client):
    response = admin_client.post(reverse("run"), {"tooltip": "foobar"})
    assert response.status_code == 200
    assert response.json() == {}


def test_run_raw(admin_client):
    response = admin_client.post(
        reverse("run"), {"command": "salt '*' cmd.run 'echo foo'"}
    )
    assert response.status_code == 200


# def test_runner(admin_client):
#     response = admin_client.get(reverse('runner'))
#     assert response.status_code == 200
#
#
# def test_runner_run(admin_client):
#     response = admin_client.post(reverse('runner'), {'function_list': 'pillar.show_top'})
#     assert response.status_code == 200
#     assert b"base" in response.content


def test_runner_raw(admin_client):
    response = admin_client.post(
        reverse("run"), {"command": "salt --client=runner pillar.show_top"}
    )
    assert response.status_code == 200
    assert b"base" in response.content


# def test_wheel(admin_client):
#     response = admin_client.get(reverse('wheel'))
#     assert response.status_code == 200


# TODO: fix wheel
# def test_wheel_run(admin_client):
#     response = admin_client.post(reverse('wheel'), {'function_list': 'key.list_all',
#                                                     'args': None})
#     print(response.content)
#     assert response.status_code == 200
#     assert b"master" in response.content
#


def test_wheel_raw(admin_client):
    response = admin_client.post(
        reverse("run"), {"command": "salt --client=wheel key.list_all"}
    )
    assert response.status_code == 200
    assert b"master" in response.content


def test_dummy_clean_out(run_sql):
    run_sql("TRUNCATE TABLE `salt_returns`")
    assert True is True
