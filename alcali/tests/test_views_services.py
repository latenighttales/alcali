from django.urls import reverse

from ..web.forms import AlcaliUserForm


def test_schedule(admin_client):
    response = admin_client.get(reverse('schedule'))
    assert response.status_code == 200


def test_schedule_list(admin_client, schedule):
    response = admin_client.post(reverse('schedule'), {"strange": "behaviour"})
    assert response.status_code == 200
    assert 'data' in response.json()
    assert response.json()['data'][0]


def test_schedule_refresh(admin_client):
    response = admin_client.post(reverse('schedule'),
                                 {'action': 'refresh', 'minion': 'master'})
    assert response.status_code == 200
    assert "job1" in response.json()['refreshed']['master']


def test_schedule_manage(admin_client, minion_master):
    response = admin_client.post(reverse('schedule'),
                                 {'action': 'disable_job',
                                  'minion': 'master',
                                  'name': 'job1'})
    assert response.status_code == 200


def test_settings(admin_client):
    response = admin_client.get(reverse('settings'))
    assert response.status_code == 200


def test_events(admin_client):
    response = admin_client.get(reverse('events'))
    assert response.status_code == 200
    assert b"salt/" in response.content


def test_users(admin_client):
    response = admin_client.get(reverse('users'))
    assert response.status_code == 200


def test_users_list(admin_client):
    response = admin_client.post(reverse('users'),
                                 {'action': 'list'})
    assert response.status_code == 200
    print(response.json()['data'][0])
    assert response.json()['data'][0]


def test_users_form_create(admin_client):
    form_data = {'username': 'foo',
                 'first_name': 'bar',
                 'last_name': 'baz',
                 'email': 'foo@example.com',
                 'password1': 'superstrongpassword',
                 'password2': 'superstrongpassword'}
    form = AlcaliUserForm(data=form_data)
    assert form.is_valid()


