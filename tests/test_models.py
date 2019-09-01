import pytest


def test_user_settings_attr(django_user_model):
    """
    All user_settings are added on create_user.
    :return:
    """
    username = "user1"
    password = "verystrongpasswordindeed"
    user1 = django_user_model.objects.create_user(username=username, password=password)
    assert hasattr(user1, "user_settings")
    attr_list = [
        "token",
        "created",
        "notifs_created",
        "notifs_published",
        "notifs_returned",
        "notifs_event",
    ]
    for attr in attr_list:
        assert hasattr(user1.user_settings, attr)


@pytest.mark.django_db
def test_conform_highstate(minion, highstate):
    highstate = highstate()
    assert minion.conformity()
    assert highstate.success_bool()


@pytest.mark.django_db
def test_not_present_highstate(minion):
    assert minion.conformity() is None


@pytest.mark.django_db
def test_not_conform_highstate(minion, highstate_diff):
    ret = highstate_diff
    assert minion.conformity() is False
