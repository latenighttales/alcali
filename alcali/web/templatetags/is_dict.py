from django import template

register = template.Library()


# Return True if variable is a dict.
#  {% if key|is_dict %}
def is_dict(var):
    return isinstance(var, dict)


register.filter("is_dict", is_dict)
