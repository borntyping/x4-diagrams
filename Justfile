economy:
  poetry run python -m x4.economy

dot:
  dot -Tpng -o docs/graphviz/economy-food-and-drugs.png docs/graphviz/economy-food-and-drugs.dot || :
  dot -Tpng -o docs/graphviz/economy-3-refined.png docs/graphviz/economy-3-refined.dot
  dot -Tpng -o docs/graphviz/economy-4-advanced.png docs/graphviz/economy-4-advanced.dot
  dot -Tpng -o docs/graphviz/economy-5-components.png docs/graphviz/economy-5-components.dot
  dot -Tpng -o docs/graphviz/economy-6-equipment.png docs/graphviz/economy-6-equipment.dot
