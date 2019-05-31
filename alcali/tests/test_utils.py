from alcali.web.utils import RawCommand


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
