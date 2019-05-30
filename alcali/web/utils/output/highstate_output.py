# -*- coding: utf-8 -*-
"""
Outputter for displaying results of state runs
==============================================

The return data from the Highstate command is a standard data structure
which is parsed by the highstate outputter to deliver a clean and readable
set of information about the HighState run on minions.

Two configurations can be set to modify the highstate outputter. These values
can be set in the master config to change the output of the ``salt`` command or
set in the minion config to change the output of the ``salt-call`` command.

state_verbose:
    By default `state_verbose` is set to `True`, setting this to `False` will
    instruct the highstate outputter to omit displaying anything in green, this
    means that nothing with a result of True and no changes will not be printed
state_output:
    The highstate outputter has five output modes, ``full``, ``terse``,
    ``mixed``, ``changes`` and ``filter``.

    * The default is set to ``full``, which will display many lines of detailed
      information for each executed chunk.
    * If ``terse`` is used, then the output is greatly simplified and shown in
      only one line.
    * If ``mixed`` is used, then terse output will be used unless a state
      failed, in which case full output will be used.
    * If ``changes`` is used, then terse output will be used if there was no
      error and no changes, otherwise full output will be used.
    * If ``filter`` is used, then either or both of two different filters can be
      used: ``exclude`` or ``terse``.
      These can be set as such from the command line, or in the Salt config as
      `state_output_exclude` or `state_output_terse`, respectively. The values to
      exclude must be a comma-separated list of `True`, `False` and/or `None`.
      Because of parsing nuances, if only one of these is used, it must still
      contain a comma. For instance: `exclude=True,`.
state_tabular:
    If `state_output` uses the terse output, set this to `True` for an aligned
    output format.  If you wish to use a custom format, this can be set to a
    string.

Example output:

.. code-block:: text

    myminion:
    ----------
              ID: test.ping
        Function: module.run
          Result: True
         Comment: Module function test.ping executed
         Changes:
                  ----------
                  ret:
                      True

    Summary
    ------------
    Succeeded: 1
    Failed:    0
    ------------
    Total:     0
"""

# Import python libs
from __future__ import absolute_import
import pprint
import textwrap

from . import nested_output


def output(data, summary=True):
    """
    The HighState Outputter is only meant to be used with the state.highstate
    function, or a function that returns highstate return data.
    """
    for host, hostdata in data.items():
        return _format_host(host, hostdata, summary)[0]


colors = {
    "GREEN": "\033[1;32;40m",
    "CYAN": "\033[1;36;40m",
    "LIGHT_RED": "\033[1;31;40m",
    "YELLOW": "\033[1;33;40m",
    "RED": "\033[1;31;40m",
    "ENDC": "\033[0;0m",
}


def _format_host(host, data, summary):
    tabular = False
    rcounts = {}
    rdurations = []
    hcolor = colors["GREEN"]
    hstrs = []
    nchanges = 0

    if isinstance(data, int) or isinstance(data, str):
        # Data in this format is from saltmod.function,
        # so it is always a 'change'
        nchanges = 1
        hstrs.append((u"{0}    {1}{2[ENDC]}".format(hcolor, data, colors)))
        hcolor = colors["CYAN"]  # Print the minion name in cyan
    if isinstance(data, list):
        # Errors have been detected, list them in RED!
        hcolor = colors["LIGHT_RED"]
        hstrs.append(
            (u"    {0}Data failed to compile:{1[ENDC]}".format(hcolor, colors))
        )
        for err in data:
            hstrs.append(
                (u"{0}----------\n    {1}{2[ENDC]}".format(hcolor, err, colors))
            )
    if isinstance(data, dict):
        # Verify that the needed data is present
        for tname, info in data.items():
            if isinstance(info, dict) and "__run_num__" not in info:
                err = (
                    u"The State execution failed to record the order "
                    "in which all states were executed. The state "
                    "return missing data is:"
                )
                hstrs.insert(0, pprint.pformat(info))
                hstrs.insert(0, err)
        # Everything rendered as it should display the output
        for tname in sorted(data, key=lambda k: data[k].get("__run_num__", 0)):
            ret = data[tname]
            # Increment result counts
            rcounts.setdefault(ret["result"], 0)
            rcounts[ret["result"]] += 1
            rduration = ret.get("duration", 0)
            try:
                rdurations.append(float(rduration))
            except ValueError:
                rduration, _, _ = rduration.partition(" ms")
                try:
                    rdurations.append(float(rduration))
                except ValueError:
                    pass
                    # log.error('Cannot parse a float from duration %s', ret.get('duration', 0))

            tcolor = colors["GREEN"]
            schanged, ctext = _format_changes(ret["changes"])
            nchanges += 1 if schanged else 0

            if schanged:
                tcolor = colors["CYAN"]
            if ret["result"] is False:
                hcolor = colors["RED"]
                tcolor = colors["RED"]
            if ret["result"] is None:
                hcolor = colors["YELLOW"]
                tcolor = colors["YELLOW"]
            comps = tname.split("_|-")
            state_lines = [
                u"{tcolor}----------{colors[ENDC]}",
                u"    {tcolor}      ID: {comps[1]}{colors[ENDC]}",
                u"    {tcolor}Function: {comps[0]}.{comps[3]}{colors[ENDC]}",
                u"    {tcolor}  Result: {ret[result]!s}{colors[ENDC]}",
                u"    {tcolor} Comment: {comment}{colors[ENDC]}",
                u"    {tcolor} Started: {ret[start_time]!s}{colors[ENDC]}",
                u"    {tcolor}Duration: {ret[duration]!s}{colors[ENDC]}",
            ]
            # This isn't the prettiest way of doing this, but it's readable.
            if comps[1] != comps[2]:
                state_lines.insert(3, u"    {tcolor}    Name: {comps[2]}{colors[ENDC]}")
            try:
                comment = ret["comment"]
                comment = comment.strip().replace(u"\n", u"\n" + u" " * 14)
            except AttributeError:  # Assume comment is a list
                try:
                    comment = ret["comment"].join(" ").replace(u"\n", u"\n" + u" " * 13)
                except AttributeError:
                    # Comment isn't a list either, just convert to string
                    comment = str(ret["comment"])
                    comment = comment.strip().replace(u"\n", u"\n" + u" " * 14)
            for detail in ["start_time", "duration"]:
                ret.setdefault(detail, u"")
            if ret["duration"] != "":
                ret["duration"] = u"{0} ms".format(ret["duration"])
            svars = {
                "tcolor": tcolor,
                "comps": comps,
                "ret": ret,
                "comment": comment,
                # This nukes any trailing \n and indents the others.
                "colors": colors,
            }
            hstrs.extend([sline.format(**svars) for sline in state_lines])
            changes = u"     Changes:   " + ctext
            hstrs.append((u"{0}{1}{2[ENDC]}".format(tcolor, changes, colors)))

            if "warnings" in ret:
                rcounts.setdefault("warnings", 0)
                rcounts["warnings"] += 1
                wrapper = textwrap.TextWrapper(
                    width=80, initial_indent=u" " * 14, subsequent_indent=u" " * 14
                )
                hstrs.append(
                    u"   {colors[LIGHT_RED]} Warnings: {0}{colors[ENDC]}".format(
                        wrapper.fill("\n".join(ret["warnings"])).lstrip(), colors=colors
                    )
                )

        # Append result counts to end of output
        colorfmt = u"{0}{1}{2[ENDC]}"
        rlabel = {
            True: u"Succeeded",
            False: u"Failed",
            None: u"Not Run",
            "warnings": u"Warnings",
        }
        count_max_len = max([len(str(x)) for x in rcounts.items()] or [0])
        label_max_len = max([len(x) for x in rlabel.items()] or [0])
        line_max_len = label_max_len + count_max_len + 2  # +2 for ': '
        if summary:
            hstrs.append(
                colorfmt.format(
                    colors["CYAN"], u"\nSummary\n{0}".format("-" * line_max_len), colors
                )
            )

            def _counts(label, count):
                return u"{0}: {1:>{2}}".format(
                    label, count, line_max_len - (len(label) + 2)
                )

            # Successful states
            changestats = []
            if None in rcounts and rcounts.get(None, 0) > 0:
                # test=True states
                changestats.append(
                    colorfmt.format(
                        colors["YELLOW"],
                        u"unchanged={0}".format(rcounts.get(None, 0)),
                        colors,
                    )
                )
            if nchanges > 0:
                changestats.append(
                    colorfmt.format(
                        colors["GREEN"], u"changed={0}".format(nchanges), colors
                    )
                )
            if changestats:
                changestats = u" ({0})".format(", ".join(changestats))
            else:
                changestats = u""
            hstrs.append(
                colorfmt.format(
                    colors["GREEN"],
                    _counts(rlabel[True], rcounts.get(True, 0) + rcounts.get(None, 0)),
                    colors,
                )
                + changestats
            )

            # Failed states
            num_failed = rcounts.get(False, 0)
            hstrs.append(
                colorfmt.format(
                    colors["RED"] if num_failed else colors["CYAN"],
                    _counts(rlabel[False], num_failed),
                    colors,
                )
            )

            num_warnings = rcounts.get("warnings", 0)
            if num_warnings:
                hstrs.append(
                    colorfmt.format(
                        colors["LIGHT_RED"],
                        _counts(rlabel["warnings"], num_warnings),
                        colors,
                    )
                )

            totals = u"{0}\nTotal states run: {1:>{2}}".format(
                "-" * line_max_len,
                sum(rcounts.values()) - rcounts.get("warnings", 0),
                line_max_len - 7,
            )
            hstrs.append(colorfmt.format(colors["CYAN"], totals, colors))
            sum_duration = sum(rdurations)
            duration_unit = "ms"
            # convert to seconds if duration is 1000ms or more
            if sum_duration > 999:
                sum_duration /= 1000
                duration_unit = "s"
            total_duration = "Total run time: {0} {1}".format(
                "{0:.3f}".format(sum_duration).rjust(line_max_len - 5), duration_unit
            )
            hstrs.append(colorfmt.format(colors["CYAN"], total_duration, colors))

    hstrs.insert(0, (u"{0}{1}:{2[ENDC]}".format(hcolor, host, colors)))
    return u"\n".join(hstrs), nchanges > 0


def _format_changes(changes):
    """
    Format the changes dict based on what the data is
    """

    if not changes:
        return False, u""

    if not isinstance(changes, dict):
        return True, u"Invalid Changes data: {0}".format(changes)

    ret = changes.get("ret")
    if ret is not None and changes.get("out") == "highstate":
        ctext = u""
        changed = False
        for host, hostdata in ret.items():
            s, c = _format_host(host, hostdata)
            ctext += u"\n" + u"\n".join((u" " * 14 + l) for l in s.splitlines())
            changed = changed or c
    else:
        changed = True
        ctext = nested_output.output(changes, nested_indent=14)
    return changed, ctext
