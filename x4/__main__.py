import pathlib

import click

from .oldeconomy import main as economy_main
from .factions import main as factions_main


@click.group()
def main():
    pass


main.add_command(economy_main)
main.add_command(factions_main)

if __name__ == "__main__":
    main()
