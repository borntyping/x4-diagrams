economy:
  rm -rf docs/graph/ docs/sankey/
  poetry run python -m x4.economy

test:
  poetry run pytest -v
