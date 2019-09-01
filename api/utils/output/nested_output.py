# -*- coding: utf-8 -*-
"""
Recursively display nested data
===============================

This is the default outputter for most execution functions.

Example output::

    myminion:
        ----------
        foo:
            ----------
            bar:
                baz
            dictionary:
                ----------
                abc:
                    123
                def:
                    456
            list:
                - Hello
                - World
"""
from __future__ import absolute_import, print_function, unicode_literals

# Import python libs
from numbers import Number

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


class NestDisplay(object):
    """
    Manage the nested display contents
    """

    def __init__(self, retcode=0):
        self.retcode = retcode
        self.LIGHT_YELLOW = "\033[1;33;40m"
        self.GREEN = "\033[1;32;40m"
        self.ENDC = "\033[0;0m"
        self.RED = "\033[1;31m"
        self.CYAN = "\033[1;36m"

    def ustring(self, indent, color, msg, prefix="", suffix="", endc=None):
        if endc is None:
            endc = self.ENDC

        indent *= " "
        fmt = "{0}{1}{2}{3}{4}{5}"

        return fmt.format(indent, color, prefix, msg, endc, suffix)

    def display(self, ret, indent, prefix, out):
        """
        Recursively iterate down through data structures to determine output
        """
        if ret is None or ret is True or ret is False:
            out.append(self.ustring(indent, self.LIGHT_YELLOW, ret, prefix=prefix))
        # Number includes all python numbers types
        #  (float, int, long, complex, ...)
        # use repr() to get the full precision also for older python versions
        # as until about python32 it was limited to 12 digits only by default
        elif isinstance(ret, Number):
            out.append(
                self.ustring(indent, self.LIGHT_YELLOW, repr(ret), prefix=prefix)
            )
        elif isinstance(ret, str):
            first_line = True
            for line in ret.splitlines():
                line_prefix = " " * len(prefix) if not first_line else prefix
                out.append(self.ustring(indent, self.GREEN, line, prefix=line_prefix))
                first_line = False
        elif isinstance(ret, (list, tuple)):
            color = self.GREEN
            if self.retcode != 0:
                color = self.RED
            for ind in ret:
                if isinstance(ind, (list, tuple, Mapping)):
                    out.append(self.ustring(indent, color, "|_"))
                    prefix = "" if isinstance(ind, Mapping) else "- "
                    self.display(ind, indent + 2, prefix, out)
                else:
                    self.display(ind, indent, "- ", out)
        elif isinstance(ret, Mapping):
            if indent:
                color = self.CYAN
                if self.retcode != 0:
                    color = self.RED
                out.append(self.ustring(indent, color, "----------"))

            # respect key ordering of ordered dicts
            if isinstance(ret, dict):
                keys = ret.keys()
            else:
                keys = sorted(ret)
            color = self.CYAN
            if self.retcode != 0:
                color = self.RED
            for key in keys:
                val = ret[key]
                out.append(self.ustring(indent, color, key, suffix=":", prefix=prefix))
                self.display(val, indent + 4, "", out)
        return out


def output(ret, **kwargs):
    """
    Display ret data
    """
    # Prefer kwargs before opts
    retcode = kwargs.get("_retcode", 0)
    base_indent = kwargs.get("nested_indent", 0)
    nest = NestDisplay(retcode=retcode)
    lines = nest.display(ret, base_indent, "", [])
    try:
        return "\n".join(lines)
    except UnicodeDecodeError:
        # output contains binary data that can't be decoded
        return str("\n").join(  # future lint: disable=blacklisted-function
            [x for x in lines]
        )
