economy:
  @rm -r "docs/"
  @mkdir "docs/"
  poetry run python -m x4.economy

test:
  poetry run pytest -v
