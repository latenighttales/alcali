import json

import yaml

from django import template

register = template.Library()


def yaml_dump(data):
    return yaml.dump(json.loads(data), default_flow_style=False)


register.filter("yaml_dump", yaml_dump)
