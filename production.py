import dataclasses
import json
import pathlib
import string
import textwrap
import typing


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


CONSTRUCTION_UNIVERSAL = {
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
} | {
    "Satellites, Resource Probes, Nav Beacons",
    "Drones and Laser Towers",
    "Missiles",
    "Mines",
    "Turret Weapons",
    "Engines and Thrusters",
    "Fixed Weapons",
    "Ship Hulls",
    "Shields",
    "Station modules",
}
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
CONSTRUCTION = (
    CONSTRUCTION_UNIVERSAL
    | CONSTRUCTION_RECYCLING_ONLY
    | CONSTRUCTION_TELADI_ONLY
    | CONSTRUCTION_TERRAN_ONLY
    | CONSTRUCTION_UNIVERSAL_ONLY
)


@dataclasses.dataclass()
class Material:
    tier: str
    name: str
    inputs: dict[str, list[str]]

    def __str__(self) -> str:
        return f"{self.tier}.{self.name}"

    def inputs_for_variant(self, variant: str) -> list[str]:
        return self.inputs.get(variant, ())


@dataclasses.dataclass()
class Production:
    materials: list[Material]
    variant: str = "Universal"
    name: str = "Production"

    def recycling(self) -> typing.Self:
        return self._replace(AGRICULTURE_UNIVERSAL | CONSTRUCTION_UNIVERSAL | CONSTRUCTION_RECYCLING_ONLY, variant="Recycling")

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

    def _filter(self, f: typing.Callable[[Material], bool]) -> list[Material]:
        return [m for m in self.materials if f(m)]

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
        mapping = {m.name: m for m in self.materials}
        for material in self.materials:
            for material_input in material.inputs_for_variant(self.variant):
                try:
                    other = mapping[material_input]
                except KeyError as error:
                    raise Exception(
                        f"{material.name} depends on {material_input}, which is missing from the {self.variant} {self.name} production chain"
                    ) from error

                if other.name in {"Water"}:
                    d2class = "produced_by_common"
                else:
                    d2class = "produced_by"

                output.append(f"{material} <- {other}: {{ class: {d2class} }}")

        path = pathlib.Path(__file__).with_name("output") / filename
        path.write_text("\n".join(output))

    @property
    def tiers(self) -> list[str]:
        present = set(m.tier for m in self.materials)
        tiers = ["Raw", "Tier 1", "Tier 2", "Tier 3", "Consumables", "Product"]
        return [t for t in tiers if t in present]

    @classmethod
    def read(cls, filename: str) -> typing.Self:
        data = json.loads(pathlib.Path(__file__).with_name(filename).read_text())
        materials = [Material(tier=m["tier"], name=m["name"], inputs=m["inputs"]) for m in data]
        return cls(materials=list(sorted(materials, key=str)))


def main():
    production = Production.read("production.json")

    agriculture_terran = production.agriculture().terran()
    agriculture_universal = production.agriculture().universal()
    construction_recycling = production.construction().recycling()
    construction_teladi = production.construction().teladi()
    construction_terran = production.construction().terran()
    construction_universal = production.construction().universal()
    terran = production.terran()

    agriculture_terran.d2("x4-agriculture-terran.d2")
    agriculture_universal.d2("x4-agriculture-universal.d2")
    construction_recycling.d2("x4-construction-recycling.d2")
    construction_teladi.d2("x4-construction-teladi.d2")
    construction_terran.d2("x4-construction-terran.d2")
    construction_universal.d2("x4-construction-universal.d2")
    terran.d2("x4-terran.d2")


if __name__ == "__main__":
    main()
