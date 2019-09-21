from datetime import timedelta
import pytest

from django.utils import timezone

from api.utils import RawCommand, graph_data, render_conformity


def test_simple_command():
    command = RawCommand("salt '*' cmd.run 'echo foobar'")
    parsed = command.parse()
    assert parsed[0]["tgt_type"] == "glob"
    assert parsed[0]["tgt"] == "*"
    assert parsed[0]["fun"] == "cmd.run"
    assert parsed[0]["client"] == "local"
    assert parsed[0]["arg"] == ["echo foobar"]


def test_simple_command_inline():
    command = RawCommand("'*' cmd.run 'echo foobar'", inline=True)
    parsed = command.parse()
    assert parsed[0]["tgt_type"] == "glob"
    assert parsed[0]["tgt"] == "*"
    assert parsed[0]["fun"] == "cmd.run"
    assert parsed[0]["client"] == "local"
    assert parsed[0]["arg"] == ["echo foobar"]


def test_complex_command():
    command = RawCommand("salt -G 'os:Fedora' cmd.run 'echo foobar' test=True")
    parsed = command.parse()
    assert parsed[0]["tgt_type"] == "grain"
    assert parsed[0]["tgt"] == "os:Fedora"
    assert parsed[0]["fun"] == "cmd.run"
    assert parsed[0]["client"] == "local"
    assert parsed[0]["arg"] == ["echo foobar", "test=True"]


def test_client():
    command = RawCommand("salt --client=runner pillar.show_top")
    parsed = command.parse()
    assert parsed[0]["fun"] == "pillar.show_top"
    assert parsed[0]["client"] == "runner"

    command = RawCommand("salt --client=runner pillar.show_top master")
    parsed = command.parse()
    assert parsed[0] == {
        "fun": "pillar.show_top",
        "client": "runner",
        "arg": ["master"],
    }

    command = RawCommand("salt --client=wheel key.list_all")
    parsed = command.parse()
    assert parsed[0] == {"fun": "key.list_all", "client": "wheel"}

    command = RawCommand("salt --client=wheel key.finger master")
    parsed = command.parse()
    assert parsed[0] == {"fun": "key.finger", "client": "wheel", "arg": ["master"]}

    command = RawCommand("salt --client=foobar key.finger master")
    parsed = command.parse()
    assert parsed == "Client not implemented: foobar"


def test_failed_cmd():
    command = RawCommand("salt '*'")
    parsed = command.parse()
    assert parsed == "Command or target not specified"


def test_batch():
    command = RawCommand("salt --client=local_batch '*' state.apply test=True -b 1")
    parsed = command.parse()
    assert parsed[0]["batch"] == "1"


def test_timeout():
    command = RawCommand("salt --client=local '*' state.apply test=True -t 9")
    parsed = command.parse()
    assert parsed[0]["timeout"] == 9


def test_client_kwarg():
    command = RawCommand("salt --client=runner pillar.show_top kwarg='{foo: bar}'")
    parsed = command.parse()
    assert parsed[0]["fun"] == "pillar.show_top"
    assert parsed[0]["client"] == "runner"
    assert "kwarg" in parsed[0]

    command = RawCommand("salt --client=wheel key.list_all kwarg='{foo: bar}'")
    parsed = command.parse()
    assert parsed[0] == {
        "fun": "key.list_all",
        "client": "wheel",
        "kwarg": "{foo: bar}",
    }


@pytest.mark.django_db
def test_graph_data():
    today = str(timezone.now().date() - timedelta(days=2))
    days, count, error_count = graph_data(period=3, fun="all")
    assert today in days


@pytest.mark.django_db
def test_render_conformity(minion_master, foo_conformity, dummy_state):
    conformity_names, ret, details = render_conformity()
    assert conformity_names == ["FOO"]
    assert ret == [{"noice": 1}]
    assert details == {"master": [{"foo": "noice"}]}
