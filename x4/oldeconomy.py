import dataclasses
import itertools
import pathlib
import string
import textwrap
import typing

import click

from x4.types import Resource
from x4_data.economy import RESOURCES

AGRICULTURE_UNIVERSAL = {
    "Ice",
    "Water",
    "BoFu",
    "BoGas",
    "Chelt Meat",
    "Food Rations",
    "Maja Dust",
    "Maja Snails",
    "Meat",
    "Medical Supplies",
    "Nostrop Oil",
    "Nostrop Oil",
    "Plankton",
    "Scruffin Fruit",
    "Soja Beans",
    "Soja Husk",
    "Space Fuel",
    "Spacefuel",
    "Spaceweed",
    "Spices",
    "Sunrise Flowers",
    "Swamp Plant",
    "Wheat",
}
AGRICULTURE_TERRAN = {
    "Ice",
    "Methane",
    "Protein Paste",
    "Terran MRE",
}
AGRICULTURE = AGRICULTURE_UNIVERSAL | AGRICULTURE_TERRAN

CONSTRUCTION_UNIVERSAL = (
    {
        "Advanced Composites",
        "Advanced Electronics",
        "Antimatter Cells",
        "Antimatter Converters",
        "Claytronics",
        "Drone Components",
        "Engine Parts",
        "Field Coils",
        "Graphene",
        "Helium",
        "Hull Parts",
        "Hydrogen",
        "Methane",
        "Microchips",
        "Missile Components",
        "Ore",
        "Plasma Conductors",
        "Quantum Tubes",
        "Scanning Arrays",
        "Shield Components",
        "Silicon Wafers",
        "Silicon",
        "Smart Chips",
        "Superfluid Coolant",
        "Turret Components",
        "Weapon Components",
    }
    | {
        "Drones",
        "Engines",
        "Laser Towers",
        "Mines",
        "Missiles",
        "Satellites",
        "Shields",
        "Ship Hulls",
        "Station Modules",
        "Thrusters",
        "Turrets",
        "Weapons",
    }
    | {"Ships", "Stations", "Deployables"}
)
CONSTRUCTION_RECYCLING_ONLY = {"Raw Scrap", "Scrap Metal"}
CONSTRUCTION_TELADI_ONLY = {"Teladianium"}
CONSTRUCTION_TERRAN_ONLY = {
    "Helium",
    "Hydrogen",
    "Methane",
    "Ore",
    "Silicon",
} | {
    "Computronic Substrate",
    "Metallic Microlattice",
    "Methane",
    "Silicon Carbide",
    "Stimulants",
}
CONSTRUCTION_UNIVERSAL_ONLY = {"Refined Metals"}
CONSTRUCTION = CONSTRUCTION_UNIVERSAL | CONSTRUCTION_RECYCLING_ONLY | CONSTRUCTION_TELADI_ONLY | CONSTRUCTION_TERRAN_ONLY | CONSTRUCTION_UNIVERSAL_ONLY


@dataclasses.dataclass()
class Production:
    materials: list[Resource]
    variant: str = "Universal"
    name: str = "Production"

    def recycling(self) -> typing.Self:
        return self._replace(
            AGRICULTURE_UNIVERSAL | CONSTRUCTION_UNIVERSAL | CONSTRUCTION_UNIVERSAL_ONLY | CONSTRUCTION_RECYCLING_ONLY,
            variant="Recycling",
        )

    def teladi(self) -> typing.Self:
        return self._replace(AGRICULTURE_UNIVERSAL | CONSTRUCTION_UNIVERSAL | CONSTRUCTION_TELADI_ONLY, variant="Teladi")

    def terran(self) -> typing.Self:
        return self._replace(AGRICULTURE_TERRAN | CONSTRUCTION_TERRAN_ONLY, variant="Terran")

    def universal(self) -> typing.Self:
        return self._replace(AGRICULTURE_UNIVERSAL | CONSTRUCTION_UNIVERSAL | CONSTRUCTION_UNIVERSAL_ONLY, variant="Universal")

    def agriculture(self) -> typing.Self:
        return self._replace(AGRICULTURE, name="Agriculture")

    def construction(self) -> typing.Self:
        return self._replace(CONSTRUCTION, name="Construction")

    def _replace(
        self,
        include: set[str] = set(),
        *,
        variant: str | None = None,
        name: str | None = None,
    ):
        return dataclasses.replace(
            self,
            materials=[m for m in self.materials if m.name in include],
            variant=variant if variant else self.variant,
            name=name if name else self.name,
        )

    def _filter(self, f: typing.Callable[[Resource], bool]) -> list[Resource]:
        return [m for m in self.materials if f(m)]

    def _get(self, name: str, for_material: Resource):
        mapping = {m.name: m for m in self.materials}
        try:
            return mapping[name]
        except KeyError as error:
            raise Exception(f"{for_material.name} depends on {name}, which is missing from the {self.variant} {self.name} production chain") from error

    def d2(self, filename: str) -> str:
        header = string.Template(
            textwrap.dedent(
                """
                direction: right
                
                                    
                classes: {
                    tier: {
                        direction: right
                    }
                    ware: {
                        shape: step
                    }
                    raw: {
                        shape: hexagon
                    }
                    product: {
                        shape: rectangle
                    }
                    consumable: {
                        shape: diamond
                    }
                    produced_by: { }
                    produced_by_common: {
                        style: {
                            stroke: grey
                            stroke-dash: 3
                        }
                    }
                }

                title: |md
                    # ${title}
                | { near: top-center }
                """
            )
        )

        # Header
        output = [header.substitute(title=f"{self.variant} {self.name}")]

        # Shapes
        for tier in self.tiers:
            output.append(f"{tier}: {{ class: tier }}")
        for material in self.materials:
            match material.tier:
                case "Raw":
                    d2class = "raw"
                case "Consumable":
                    d2class = "consumable"
                case "Product":
                    d2class = "product"
                case _:
                    d2class = "ware"
            output.append(f"{material}: {{ class: {d2class} }}")
        output.append("")

        # Connections
        for material in self.materials:
            for other_name in material.inputs_for_variant(self.variant):
                other = self._get(other_name, for_material=material)

                if other.name in {"Water"}:
                    d2class = "produced_by_common"
                else:
                    d2class = "produced_by"

                output.append(f"{material} <- {other}: {{ class: {d2class} }}")

        path = pathlib.Path(__file__).with_name("output") / filename
        path.write_text("\n".join(output))

    def dot(self) -> str:
        return ""

    def write(self, output_directory: pathlib.Path, filename: str):
        (output_directory / filename).write_text(self.dot())
        return

    def old(self, output_directory: pathlib.Path, filename: str):
        with (output_directory / filename).open("w") as file:
            print("digraph {", file=file)
            print('  fontname="Helvetica,Arial,sans-serif"', file=file)
            print('  graph [pad="0.5", ranksep="2", nodesep="0.3"];', file=file)
            print(
                '  node [fontname="Helvetica,Arial,sans-serif",penwidth="0",style="filled",linecolor="black",margin="0.2"]',
                file=file,
            )
            print('  edge [fontname="Helvetica,Arial,sans-serif",penwidth="2.5"]', file=file)

            for tier, materials in itertools.groupby(self.materials, key=lambda m: m.tier):
                print(f"  subgraph {tier.id} {{", file=file)
                print(f"    cluster = true;", file=file)
                print(f'    label = "{tier.name}";', file=file)
                for material in materials:
                    print(
                        f'    node [label="{material.name}",shape="box",fillcolor="{material.node_colour}"] {material.id};',
                        file=file,
                    )
                print("  }", file=file)

            for material in self.materials:
                for other_name in material.inputs_for_variant(self.variant):
                    other = self._get(other_name, for_material=material)
                    print(f'  {other.id} -> {material.id} [color="{other.node_colour}"];', file=file)

            print("}", file=file)

    @property
    def tiers(self) -> list[str]:
        return list(sorted(set(m.tier for m in self.materials)))

    @classmethod
    def read(cls, filename: str) -> typing.Self:
        return cls(materials=list(sorted(RESOURCES, key=str)))


@click.command(name="economy")
@click.option(
    "--output-directory",
    default="output",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        path_type=pathlib.Path,
    ),
)
def main(output_directory: pathlib.Path):
    output_directory.mkdir(exist_ok=True)

    production = Production.read("production.json")

    agriculture_terran = production.agriculture().terran()
    agriculture_universal = production.agriculture().universal()
    construction_recycling = production.construction().recycling()
    construction_teladi = production.construction().teladi()
    construction_terran = production.construction().terran()
    construction_universal = production.construction().universal()
    terran = production.terran()

    agriculture_terran.dot(output_directory, "x4-agriculture-terran.dot")
    agriculture_universal.dot(output_directory, "x4-agriculture-universal.dot")
    construction_recycling.dot(output_directory, "x4-construction-recycling.dot")
    construction_teladi.dot(output_directory, "x4-construction-teladi.dot")
    construction_terran.dot(output_directory, "x4-construction-terran.dot")
    construction_universal.dot(output_directory, "x4-construction-universal.dot")
    terran.dot(output_directory, "x4-terran.dot")
    production.dot(output_directory, "x4.dot")


if __name__ == "__main__":
    main()
