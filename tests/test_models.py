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


@pytest.mark.django_db
def test_failed_highstate(minion, highstate_failed):
    assert minion.conformity() is False


@pytest.mark.django_db
def test_custom_conformity_false(minion_master):
    assert minion_master.custom_conformity("cmd.run", "alcali --version") == False


@pytest.mark.django_db
def test_custom_conformity(minion_master, alcali_version_state, version_conformity):
    assert minion_master.custom_conformity("cmd.run", "alcali --version") == "2019.2.2"


@pytest.mark.django_db
def test_salt_return_job_args(jobs_arguments):
    assert jobs_arguments.arguments() == "foo 1 bar=baz"
