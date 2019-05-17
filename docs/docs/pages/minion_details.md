# Minion Detail

(screenshot)
## Infos and Network

All those details are parsed from `grain.items` except conformity.(see [conformity](conformity.md) for more infos).

By default, the right section contains only:

 - GRAIN: `grains.items`
 - PILLAR: `pillar.items`
 - HISTORY: Last 100 jobs for this minion.
 - GRAPH: Filtered for this minion.

You can add more section by adding some [minion custom fields](settings.md).

We recommend adding:

 - HIGHSTATE: `state.show_highstate`
 - TOP FILE: `state.show_top`