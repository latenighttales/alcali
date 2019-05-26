from alcali.web.templatetags.getattribute import getattribute
from alcali.web.templatetags.is_dict import is_dict
from alcali.web.templatetags.yaml_dump import yaml_dump


def test_getattribute_dict():
    foo = {"bar": True}
    assert getattribute(foo, "bar")


def test_getattribute_obj():
    class Foo:
        pass

    foo = Foo()
    foo.bar = True
    assert getattribute(foo, "bar")


def test_getattribute_list():
    foo = ["bar", "baz", "spam"]
    assert getattribute(foo, "1")


def test_is_dict():
    foo = {"bar": True}
    assert is_dict(foo)
    bar = ["bar", "baz", "spam"]
    assert is_dict(bar) is False


def test_yaml_dump():
    foo = '{"bar": [true, false]}'
    assert yaml_dump(foo) == "bar:\n- true\n- false\n"
