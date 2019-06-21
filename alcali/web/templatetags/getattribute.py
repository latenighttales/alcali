import re
from django import template

numeric_test = re.compile(r"^\d+$")
register = template.Library()


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name
    it first does a standard attribute look-up, then tries to do a dictionary look-up,
    then tries a getitem lookup (for lists to work),
    then follows standard Django template behavior when an object is not found."""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    if hasattr(value, "has_key") and value in arg:
        return value[arg]
    if numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    return value[arg]


register.filter("getattribute", getattribute)
