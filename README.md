x4-diagrams
===========

Diagrams illustrating [X4] faction relationships and economy flows.

This project is entirely unaffiliated with Egosoft.

Usage
-----

```shell
python -m x4 --help
python -m x4.factions
python -m x4.economy
```

Graphviz `dot` files will be written to an `output/` directory.

Data
----

I've used [Economy Flow Charts - X4 Foundations Wiki] as the reference for grouping wares into "tiers". The only change I've made was to move Scanning Arrays from tier 5 to tier 4, which made several diagrams much simpler.

References
----------

* [Economy Flow Charts - X4 Foundations Wiki]
* [X4 Station Calculator](http://www.x4-game.com) by [@crissian](https://github.com/crissian)
  * In particular, [wares-data.ts](https://github.com/crissian/x4/blob/dev/src/app/shared/services/data/wares-data.ts) was used as a starting point for the [x4_data.economy](./x4_data/economy.py) module.
* [X4 Production Chart](https://x4prodchart.com/) by [Abraham Zakharov](https://abrahamzakharov.com/)
* [Production Chain Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1585211529) by [PyroChiliarch](https://steamcommunity.com/id/PyroChiliarch)
* [Wares - Roguey's X4 site](https://roguey.co.uk/x4/wares/) by [Roguey](https://roguey.co.uk)
* [X4: Foundations](http://www.x4-game.com) by [Egosoft](https://www.egosoft.com)


[X4]: https://store.steampowered.com/app/392160/X4_Foundations/
[Economy Flow Charts - X4 Foundations Wiki]: https://wiki.egosoft.com:1337/X4%20Foundations%20Wiki/Manual%20and%20Guides/Objects%20in%20the%20Game%20Universe/Economy%20Flow%20Charts/ 
