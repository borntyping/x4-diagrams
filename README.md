x4-diagrams
===========

Diagrams illustrating [X4] faction relationships and economy flows.

## Graphs

<img src="./docs/graph/economy-3-refined.png" alt="" style="width: 500px;">
<img src="./docs/graph/economy-4-advanced.png" alt="" style="width: 500px;">
<img src="./docs/graph/economy-5-components.png" alt="" style="width: 500px;">
<img src="./docs/graph/economy-6-equipment.png" alt="" style="width: 500px;">
<img src="./docs/graph/economy-food-and-drugs.png" alt="" style="width: 500px;">

## Sankey diagrams

<img src="./docs/sankey/economy-construction.png" alt="" style="width: 500px;">
<img src="./docs/sankey/economy-food-and-drugs.png" alt="" style="width: 500px;">
<img src="./docs/sankey/economy-3-refined.png" alt="" style="width: 500px;">
<img src="./docs/sankey/economy-4-advanced.png" alt="" style="width: 500px;">
<img src="./docs/sankey/economy-5-components.png" alt="" style="width: 500px;">
<img src="./docs/sankey/economy-6-equipment.png" alt="" style="width: 500px;">

Usage
-----

```shell
python -m x4 --help
python -m x4.factions
python -m x4.economy
```

Graphviz `dot` files will be written to an `output/` directory.

References
----------

* https://wiki.egosoft.com:1337/X4%20Foundations%20Wiki/Manual%20and%20Guides/Objects%20in%20the%20Game%20Universe/Economy%20Flow%20Charts/
* https://x4prodchart.com/
* https://steamcommunity.com/sharedfiles/filedetails/?id=1585211529
* https://roguey.co.uk/x4/wares/
* http://www.x4-game.com
  * https://github.com/crissian/x4/blob/dev/src/app/shared/services/data/wares-data.ts

[X4]: https://store.steampowered.com/app/392160/X4_Foundations/
