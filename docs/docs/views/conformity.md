# Conformity

![conformity](../images/conformity_view.png)

## Highstate

Highstate conformity will schedule a job named **highstate_conformity** on selected targets.

The function used is `#!python state.apply test=True`.

You can use salt targeting syntax, e.g: `-G 'os:Fedora'`.

By default, it will target all minions (`'*'`).

## Custom

Custom conformity will parse the supplied function in minions job history and provide the result on the [overview](overview.md#conformity) page.

To be meaningful, you should run the function regularly (e.g. scheduling a recurring job).