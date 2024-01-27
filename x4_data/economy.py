import typing

from x4.colours import Palette
from x4.types import RecipeInput, Method, Recipe, Tier, Ware
from x4_data.races import ARGON, BORON, PARANID, SPLIT, TELADI, TERRAN

COMMONWEALTH: typing.Sequence[Method] = (
    "Universal",
    "Argon",
    "Boron",
    "Paranid",
    "Split",
    "Teladi",
)

TIER_0 = Tier(key=0, name="Harvested", colour=Palette.GREY)
TIER_1 = Tier(key=1, name="Basic Food", colour=Palette.GREY)
TIER_2 = Tier(key=2, name="Food and Drugs", colour=Palette.GREY)
TIER_3 = Tier(key=3, name="Refined", colour=Palette.GREY)
TIER_4 = Tier(key=4, name="Advanced", colour=Palette.GREY)
TIER_5 = Tier(key=5, name="Components", colour=Palette.GREY)
TIER_6 = Tier(key=6, name="Equipment", colour=Palette.PURPLE)

WARES_TIER_0 = (
    Ware(
        key="helium",
        name="Helium",
        acronym="He",
        tier=TIER_0,
        colour=Palette.TEAL,
        volume=6,
        storage="Liquid",
        price_min=37,
        price_avg=44,
        price_max=51,
        recipes=[],
    ),
    Ware(
        key="methane",
        name="Methane",
        acronym="Me",
        tier=TIER_0,
        colour=Palette.LIME,
        volume=6,
        storage="Liquid",
        price_min=41,
        price_avg=48,
        price_max=55,
        recipes=[],
    ),
    Ware(
        key="ore",
        name="Ore",
        acronym="Or",
        tier=TIER_0,
        colour=Palette.RED,
        volume=10,
        storage="Solid",
        price_min=43,
        price_avg=50,
        price_max=58,
        recipes=[],
    ),
    Ware(
        key="hydrogen",
        name="Hydrogen",
        acronym="Hy",
        tier=TIER_0,
        colour=Palette.CYAN,
        volume=6,
        storage="Liquid",
        price_min=49,
        price_avg=58,
        price_max=67,
        recipes=[],
    ),
    Ware(
        key="silicon",
        name="Silicon",
        acronym="Si",
        tier=TIER_0,
        colour=Palette.LIME,
        volume=10,
        storage="Solid",
        price_min=111,
        price_avg=130,
        price_max=150,
        recipes=[],
    ),
    Ware(
        key="nividium",
        name="Nividium",
        acronym="Nv",
        tier=TIER_0,
        colour=Palette.MAGENTA,
        volume=10,
        storage="Solid",
        price_min=434,
        price_avg=510,
        price_max=587,
        recipes=[],
    ),
    Ware(
        key="ice",
        name="Ice",
        acronym="Ic",
        tier=TIER_0,
        colour=Palette.BLUE,
        volume=8,
        storage="Solid",
        price_min=26,
        price_avg=30,
        price_max=35,
        recipes=[],
    ),
    Ware(
        key="raw_scrap",
        name="Raw Scrap",
        acronym="RS",
        tier=TIER_0,
        colour=Palette.BROWN,
        volume=10,
        storage="Solid",
        price_min=153,
        price_avg=180,
        price_max=207,
        recipes=[],
    ),
    Ware(
        key="scrap_metal",
        name="Scrap Metal",
        acronym="SM",
        tier=TIER_0,
        colour=Palette.BROWN,
        volume=10,
        storage="Solid",
        price_min=318,
        price_avg=375,
        price_max=431,
        recipes=[
            Recipe(
                time=60,
                amount=1,
                method="Recycling",
                inputs=(
                    RecipeInput("energy_cells", 10),
                    RecipeInput("raw_scrap", 1),
                ),
            )
        ],
    ),
    Ware(
        key="water",
        name="Water",
        acronym="Wt",
        tier=TIER_0,
        colour=Palette.BLUE,
        volume=6,
        storage="Container",
        price_min=32,
        price_avg=53,
        price_max=74,
        recipes=[
            Recipe(
                time=120,
                amount=193,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("ice", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="energy_cells",
        name="Energy Cells",
        acronym="EC",
        tier=TIER_0,
        colour=Palette.GREY,
        volume=1,
        storage="Container",
        price_min=10,
        price_avg=16,
        price_max=22,
        recipes=[
            Recipe(
                time=60,
                amount=175,
                method="Universal",
                inputs=(),
            ),
            Recipe(
                time=60,
                amount=50,
                method="Terran",
                inputs=(),
            ),
        ],
    ),
)

WARES_TIER_1 = (
    Ware(
        key="maja_snails",
        name="Maja Snails",
        acronym="MS",
        tier=TIER_1,
        colour=PARANID.colour,
        volume=6,
        storage="Container",
        price_min=35,
        price_avg=58,
        price_max=81,
        recipes=[
            Recipe(
                time=450,
                amount=146,
                method="Paranid",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("water", 100),
                ),
            ),
        ],
    ),
    Ware(
        key="meat",
        name="Meat",
        acronym="Mt",
        tier=TIER_1,
        colour=ARGON.colour,
        volume=6,
        storage="Container",
        price_min=29,
        price_avg=48,
        price_max=68,
        recipes=[
            Recipe(
                time=450,
                amount=290,
                method="Argon",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("water", 100),
                ),
            ),
        ],
    ),
    Ware(
        key="soja_beans",
        name="Soja Beans",
        acronym="SB",
        tier=TIER_1,
        colour=PARANID.colour,
        volume=5,
        storage="Container",
        price_min=40,
        price_avg=67,
        price_max=93,
        recipes=[
            Recipe(
                time=300,
                amount=104,
                method="Paranid",
                inputs=(
                    RecipeInput("energy_cells", 30),
                    RecipeInput("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="spices",
        name="Spices",
        acronym="Sp",
        tier=TIER_1,
        colour=Palette.BLACK,
        volume=3,
        storage="Container",
        price_min=12,
        price_avg=20,
        price_max=28,
        recipes=[
            Recipe(
                time=600,
                amount=500,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="sunrise_flowers",
        name="Sunrise Flowers",
        acronym="SF",
        tier=TIER_1,
        colour=TELADI.colour,
        volume=5,
        storage="Container",
        price_min=48,
        price_avg=80,
        price_max=112,
        recipes=[
            Recipe(
                time=300,
                amount=100,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 30),
                    RecipeInput("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="swamp_plant",
        name="Swamp Plant",
        acronym="SP",
        tier=TIER_1,
        colour=TELADI.colour,
        volume=6,
        storage="Container",
        price_min=50,
        price_avg=84,
        price_max=117,
        recipes=[
            Recipe(
                time=450,
                amount=120,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("water", 100),
                ),
            ),
        ],
    ),
    Ware(
        key="wheat",
        name="Wheat",
        acronym="Wh",
        tier=TIER_1,
        colour=ARGON.colour,
        volume=4,
        storage="Container",
        price_min=19,
        price_avg=31,
        price_max=44,
        recipes=[
            Recipe(
                time=300,
                amount=310,
                method="Argon",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="chelt_meat",
        name="Chelt Meat",
        acronym="CM",
        tier=TIER_1,
        colour=SPLIT.colour,
        volume=7,
        storage="Container",
        price_min=31,
        price_avg=51,
        price_max=72,
        recipes=[
            Recipe(
                time=450,
                amount=209,
                method="Split",
                inputs=(
                    RecipeInput("energy_cells", 50),
                    RecipeInput("water", 120),
                ),
            ),
        ],
    ),
    Ware(
        key="scruffin_fruits",
        name="Scruffin Fruit",
        acronym="SF",
        tier=TIER_1,
        colour=SPLIT.colour,
        volume=6,
        storage="Container",
        price_min=17,
        price_avg=28,
        price_max=40,
        recipes=[
            Recipe(
                time=300,
                amount=255,
                method="Split",
                inputs=(
                    RecipeInput("energy_cells", 30),
                    RecipeInput("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="protein_paste",
        name="Protein Paste",
        acronym="PP",
        tier=TIER_1,
        colour=TERRAN.colour,
        volume=4,
        storage="Container",
        price_min=57,
        price_avg=96,
        price_max=134,
        recipes=[
            Recipe(
                time=300,
                amount=219,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("ice", 80),
                    RecipeInput("methane", 200),
                ),
            )
        ],
    ),
    Ware(
        key="plankton",
        name="Plankton",
        acronym="Pl",
        tier=TIER_1,
        colour=BORON.colour,
        volume=1,
        storage="Container",
        price_min=11,
        price_avg=18,
        price_max=25,
        recipes=[
            Recipe(
                time=400,
                amount=275,
                method="Boron",
                inputs=(
                    RecipeInput("energy_cells", 20),
                    RecipeInput("water", 50),
                ),
            ),
        ],
    ),
    Ware(
        key="bogas",
        name="BoGas",
        acronym="BG",
        tier=TIER_1,
        colour=BORON.colour,
        volume=4,
        storage="Container",
        price_min=44,
        price_avg=73,
        price_max=102,
        recipes=[
            Recipe(
                time=150,
                amount=110,
                method="Boron",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("water", 100),
                ),
            ),
        ],
    ),
)

WARES_TIER_2 = (
    Ware(
        key="spacefuel",
        name="Spacefuel",
        acronym="SF",
        tier=TIER_2,
        colour=ARGON.colour,
        volume=2,
        storage="Container",
        price_min=60,
        price_avg=133,
        price_max=207,
        recipes=[
            Recipe(
                time=480,
                amount=98,
                method="Argon",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("water", 100),
                    RecipeInput("wheat", 80),
                ),
            )
        ],
    ),
    Ware(
        key="food_rations",
        name="Food Rations",
        acronym="FR",
        tier=TIER_2,
        colour=ARGON.colour,
        volume=1,
        storage="Container",
        price_min=12,
        price_avg=21,
        price_max=29,
        recipes=[
            Recipe(
                time=240,
                amount=460,
                method="Argon",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("meat", 40),
                    RecipeInput("spices", 40),
                    RecipeInput("wheat", 40),
                ),
            )
        ],
    ),
    Ware(
        key="maja_dust",
        name="Maja Dust",
        acronym="MD",
        tier=TIER_2,
        colour=PARANID.colour,
        volume=6,
        storage="Container",
        price_min=94,
        price_avg=208,
        price_max=323,
        recipes=[
            Recipe(
                time=600,
                amount=64,
                method="Paranid",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("maja_snails", 120),
                    RecipeInput("spices", 60),
                ),
            )
        ],
    ),
    Ware(
        key="soja_husk",
        name="Soja Husk",
        acronym="SH",
        tier=TIER_2,
        colour=PARANID.colour,
        volume=1,
        storage="Container",
        price_min=19,
        price_avg=32,
        price_max=45,
        recipes=[
            Recipe(
                time=300,
                amount=350,
                method="Paranid",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("maja_snails", 50),
                    RecipeInput("soja_beans", 40),
                    RecipeInput("spices", 20),
                ),
            )
        ],
    ),
    Ware(
        key="spaceweed",
        name="Spaceweed",
        acronym="SW",
        tier=TIER_2,
        colour=TELADI.colour,
        volume=3,
        storage="Container",
        price_min=75,
        price_avg=166,
        price_max=257,
        recipes=[
            Recipe(
                time=600,
                amount=183,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 140),
                    RecipeInput("spices", 40),
                    RecipeInput("swamp_plant", 120),
                ),
            )
        ],
    ),
    Ware(
        key="nostrop_oil",
        name="Nostrop Oil",
        acronym="NO",
        tier=TIER_2,
        colour=TELADI.colour,
        volume=1,
        storage="Container",
        price_min=20,
        price_avg=34,
        price_max=47,
        recipes=[
            Recipe(
                time=300,
                amount=500,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("spices", 40),
                    RecipeInput("sunrise_flowers", 40),
                    RecipeInput("water", 60),
                ),
            )
        ],
    ),
    Ware(
        key="medical_supplies",
        name="Medical Supplies",
        acronym="MS",
        tier=TIER_2,
        colour=Palette.BLACK,
        volume=2,
        storage="Container",
        price_min=43,
        price_avg=66,
        price_max=89,
        recipes=[
            Recipe(
                time=300,
                amount=208,
                method="Argon",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("spices", 40),
                    RecipeInput("water", 60),
                    RecipeInput("wheat", 30),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Paranid",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("soja_beans", 10),
                    RecipeInput("spices", 40),
                    RecipeInput("water", 60),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("spices", 40),
                    RecipeInput("sunrise_flowers", 12),
                    RecipeInput("water", 60),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Split",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("scruffin_fruits", 30),
                    RecipeInput("spices", 60),
                    RecipeInput("water", 60),
                ),
            ),
            Recipe(
                time=300,
                amount=140,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("ice", 50),
                    RecipeInput("protein_paste", 24),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Boron",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("plankton", 95),
                    RecipeInput("water", 60),
                ),
            ),
        ],
    ),
    Ware(
        key="terran_mre",
        name="Terran MRE",
        acronym="TM",
        tier=TIER_2,
        colour=TERRAN.colour,
        volume=2,
        storage="Container",
        price_min=32,
        price_avg=54,
        price_max=75,
        recipes=[
            Recipe(
                time=240,
                amount=175,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("protein_paste", 60),
                ),
            )
        ],
    ),
    Ware(
        key="stimulants",
        name="Stimulants",
        acronym="St",
        tier=TIER_2,
        colour=TERRAN.colour,
        volume=12,
        storage="Container",
        price_min=153,
        price_avg=340,
        price_max=527,
        recipes=[
            Recipe(
                time=300,
                amount=98,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("helium", 400),
                    RecipeInput("silicon", 20),
                ),
            )
        ],
    ),
    Ware(
        key="bofu",
        name="BoFu",
        acronym="BF",
        tier=TIER_2,
        colour=BORON.colour,
        volume=4,
        storage="Container",
        price_min=61,
        price_avg=101,
        price_max=142,
        recipes=[
            Recipe(
                time=240,
                amount=82,
                method="Boron",
                inputs=(
                    RecipeInput("bogas", 40),
                    RecipeInput("energy_cells", 40),
                    RecipeInput("plankton", 120),
                ),
            )
        ],
    ),
)

WARES_TIER_3 = (
    Ware(
        key="superfluid_coolant",
        name="Superfluid Coolant",
        acronym="SC",
        tier=TIER_3,
        colour=Palette.CYAN,
        volume=16,
        storage="Container",
        price_min=90,
        price_avg=150,
        price_max=211,
        recipes=[
            Recipe(
                time=240,
                amount=95,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("helium", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="graphene",
        name="Graphene",
        acronym="Gr",
        tier=TIER_3,
        colour=Palette.BLACK,
        volume=20,
        storage="Container",
        price_min=100,
        price_avg=166,
        price_max=233,
        recipes=[
            Recipe(
                time=240,
                amount=96,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("methane", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="refined_metals",
        name="Refined Metals",
        acronym="RM",
        tier=TIER_3,
        colour=Palette.MAROON,
        volume=14,
        storage="Container",
        price_min=89,
        price_avg=148,
        price_max=207,
        recipes=[
            Recipe(
                time=150,
                amount=88,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 90),
                    RecipeInput("ore", 240),
                ),
            ),
        ],
    ),
    Ware(
        key="teladianium",
        name="Teladianium",
        acronym="Tl",
        tier=TIER_3,
        colour=Palette.YELLOW,
        volume=16,
        storage="Container",
        price_min=121,
        price_avg=202,
        price_max=283,
        recipes=[
            Recipe(
                time=120,
                amount=70,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 45),
                    RecipeInput("ore", 280),
                ),
            ),
        ],
    ),
    Ware(
        key="antimatter_cells",
        name="Antimatter Cells",
        acronym="AC",
        tier=TIER_3,
        colour=Palette.LAVENDER,
        volume=18,
        storage="Container",
        price_min=121,
        price_avg=202,
        price_max=282,
        recipes=[
            Recipe(
                time=120,
                amount=99,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 100),
                    RecipeInput("hydrogen", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="silicon_wafers",
        name="Silicon Wafers",
        acronym="SW",
        tier=TIER_3,
        colour=Palette.MINT,
        volume=18,
        storage="Container",
        price_min=180,
        price_avg=299,
        price_max=419,
        recipes=[
            Recipe(
                time=180,
                amount=107,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 90),
                    RecipeInput("silicon", 240),
                ),
            ),
        ],
    ),
    Ware(
        key="computronic_substrate",
        name="Computronic Substrate",
        acronym="CS",
        tier=TIER_3,
        colour=Palette.BLUE,
        volume=50,
        storage="Container",
        price_min=7452,
        price_avg=8280,
        price_max=9108,
        recipes=[
            Recipe(
                time=600,
                amount=98,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 4000),
                    RecipeInput("hydrogen", 2000),
                    RecipeInput("ore", 3000),
                    RecipeInput("silicon", 3000),
                ),
            ),
            Recipe(
                time=300,
                amount=50,
                method="Recycling",
                inputs=(
                    RecipeInput("energy_cells", 12500),
                    RecipeInput("scrap_metal", 1000),
                ),
            ),
        ],
    ),
    Ware(
        key="metallic_microlattice",
        name="Metallic Microlattice",
        acronym="MM",
        tier=TIER_3,
        colour=Palette.CYAN,
        volume=1,
        storage="Container",
        price_min=42,
        price_avg=50,
        price_max=57,
        recipes=[
            Recipe(
                time=180,
                amount=190,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 50),
                    RecipeInput("helium", 130),
                    RecipeInput("ore", 50),
                ),
            )
        ],
    ),
)

WARES_TIER_4 = (
    Ware(
        key="plasma_conductors",
        name="Plasma Conductors",
        acronym="PC",
        tier=TIER_4,
        colour=Palette.OLIVE,
        volume=32,
        storage="Container",
        price_min=769,
        price_avg=1026,
        price_max=1282,
        recipes=[
            Recipe(
                time=900,
                amount=44,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("graphene", 96),
                    RecipeInput("superfluid_coolant", 140),
                ),
            )
        ],
    ),
    Ware(
        key="quantum_tubes",
        name="Quantum Tubes",
        acronym="QT",
        tier=TIER_4,
        colour=Palette.MAGENTA,
        volume=22,
        storage="Container",
        price_min=225,
        price_avg=300,
        price_max=375,
        recipes=[
            Recipe(
                time=720,
                amount=94,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 40),
                    RecipeInput("graphene", 116),
                    RecipeInput("superfluid_coolant", 30),
                ),
            )
        ],
    ),
    Ware(
        key="advanced_composites",
        name="Advanced Composites",
        acronym="AC",
        tier=TIER_4,
        colour=Palette.APRICOT,
        volume=32,
        storage="Container",
        price_min=432,
        price_avg=540,
        price_max=648,
        recipes=[
            Recipe(
                time=300,
                amount=54,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 50),
                    RecipeInput("graphene", 80),
                    RecipeInput("refined_metals", 80),
                ),
            ),
            Recipe(
                time=300,
                amount=54,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 50),
                    RecipeInput("graphene", 80),
                    RecipeInput("teladianium", 58),
                ),
            ),
        ],
    ),
    Ware(
        key="hull_parts",
        name="Hull Parts",
        acronym="HP",
        tier=TIER_4,
        colour=Palette.RED,
        volume=12,
        storage="Container",
        price_min=146,
        price_avg=209,
        price_max=272,
        recipes=[
            Recipe(
                time=900,
                amount=294,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("graphene", 40),
                    RecipeInput("refined_metals", 280),
                ),
            ),
            Recipe(
                time=300,
                amount=200,
                method="Recycling",
                inputs=(
                    RecipeInput("energy_cells", 3500),
                    RecipeInput("scrap_metal", 75),
                ),
            ),
            Recipe(
                time=900,
                amount=294,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 80),
                    RecipeInput("graphene", 40),
                    RecipeInput("teladianium", 204),
                ),
            ),
        ],
    ),
    Ware(
        key="engine_parts",
        name="Engine Parts",
        acronym="EP",
        tier=TIER_4,
        colour=Palette.BLUE,
        volume=15,
        storage="Container",
        price_min=128,
        price_avg=182,
        price_max=237,
        recipes=[
            Recipe(
                time=900,
                amount=208,
                method="Universal",
                inputs=(
                    RecipeInput("antimatter_cells", 80),
                    RecipeInput("energy_cells", 60),
                    RecipeInput("refined_metals", 96),
                ),
            ),
            Recipe(
                time=900,
                amount=208,
                method="Teladi",
                inputs=(
                    RecipeInput("antimatter_cells", 80),
                    RecipeInput("energy_cells", 60),
                    RecipeInput("teladianium", 70),
                ),
            ),
        ],
    ),
    Ware(
        key="microchips",
        name="Microchips",
        acronym="Mc",
        tier=TIER_4,
        colour=Palette.GREEN,
        volume=22,
        storage="Container",
        price_min=805,
        price_avg=948,
        price_max=1090,
        recipes=[
            Recipe(
                time=600,
                amount=72,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 50),
                    RecipeInput("silicon_wafers", 200),
                ),
            )
        ],
    ),
    Ware(
        key="smart_chips",
        name="Smart Chips",
        acronym="SC",
        tier=TIER_4,
        colour=Palette.MINT,
        volume=2,
        storage="Container",
        price_min=46,
        price_avg=57,
        price_max=69,
        recipes=[
            Recipe(
                time=600,
                amount=143,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 50),
                    RecipeInput("silicon_wafers", 20),
                ),
            )
        ],
    ),
    Ware(
        key="silicon_carbide",
        name="Silicon Carbide",
        acronym="SC",
        tier=TIER_4,
        colour=Palette.NAVY,
        volume=20,
        storage="Container",
        price_min=1202,
        price_avg=1414,
        price_max=1627,
        recipes=[
            Recipe(
                time=300,
                amount=48,
                method="Terran",
                inputs=(
                    RecipeInput("energy_cells", 200),
                    RecipeInput("metallic_microlattice", 2),
                    RecipeInput("methane", 400),
                    RecipeInput("silicon", 300),
                ),
            ),
            Recipe(
                time=300,
                amount=60,
                method="Recycling",
                inputs=(
                    RecipeInput("energy_cells", 4000),
                    RecipeInput("scrap_metal", 250),
                ),
            ),
        ],
    ),
)

WARES_TIER_5 = (
    Ware(
        key="drone_components",
        name="Drone Components",
        acronym="DC",
        tier=TIER_5,
        colour=Palette.PINK,
        volume=30,
        storage="Container",
        price_min=685,
        price_avg=914,
        price_max=1142,
        recipes=[
            Recipe(
                time=1200,
                amount=105,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("engine_parts", 20),
                    RecipeInput("hull_parts", 20),
                    RecipeInput("microchips", 20),
                    RecipeInput("scanning_arrays", 40),
                ),
            )
        ],
    ),
    Ware(
        key="turret_components",
        name="Turret Components",
        acronym="TC",
        tier=TIER_5,
        colour=Palette.APRICOT,
        volume=20,
        storage="Container",
        price_min=164,
        price_avg=273,
        price_max=383,
        recipes=[
            Recipe(
                time=1800,
                amount=170,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("microchips", 20),
                    RecipeInput("quantum_tubes", 20),
                    RecipeInput("scanning_arrays", 10),
                ),
            )
        ],
    ),
    Ware(
        key="missile_components",
        name="Missile Components",
        acronym="MC",
        tier=TIER_5,
        colour=Palette.BEIGE,
        volume=2,
        storage="Container",
        price_min=6,
        price_avg=9,
        price_max=13,
        recipes=[
            Recipe(
                time=900,
                amount=281,
                method="Universal",
                inputs=(
                    RecipeInput("advanced_composites", 2),
                    RecipeInput("energy_cells", 20),
                    RecipeInput("hull_parts", 2),
                ),
            )
        ],
    ),
    Ware(
        key="field_coils",
        name="Field Coils",
        acronym="FC",
        tier=TIER_5,
        colour=Palette.MINT,
        volume=15,
        storage="Container",
        price_min=247,
        price_avg=412,
        price_max=576,
        recipes=[
            Recipe(
                time=600,
                amount=175,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("plasma_conductors", 40),
                    RecipeInput("quantum_tubes", 43),
                ),
            )
        ],
    ),
    Ware(
        key="shield_components",
        name="Shield Components",
        acronym="SC",
        tier=TIER_5,
        colour=Palette.LAVENDER,
        volume=10,
        storage="Container",
        price_min=113,
        price_avg=188,
        price_max=264,
        recipes=[
            Recipe(
                time=1200,
                amount=193,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 70),
                    RecipeInput("plasma_conductors", 20),
                    RecipeInput("quantum_tubes", 20),
                ),
            )
        ],
    ),
    Ware(
        key="antimatter_converters",
        name="Antimatter Converters",
        acronym="AC",
        tier=TIER_5,
        colour=Palette.MAGENTA,
        volume=10,
        storage="Container",
        price_min=248,
        price_avg=354,
        price_max=461,
        recipes=[
            Recipe(
                time=300,
                amount=133,
                method="Universal",
                inputs=(
                    RecipeInput("advanced_composites", 20),
                    RecipeInput("energy_cells", 80),
                    RecipeInput("microchips", 30),
                ),
            )
        ],
    ),
    Ware(
        key="weapon_components",
        name="Weapon Components",
        acronym="WC",
        tier=TIER_5,
        colour=Palette.CYAN,
        volume=20,
        storage="Container",
        price_min=171,
        price_avg=285,
        price_max=399,
        recipes=[
            Recipe(
                time=1800,
                amount=170,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("hull_parts", 20),
                    RecipeInput("plasma_conductors", 30),
                ),
            )
        ],
    ),
    Ware(
        key="scanning_arrays",
        name="Scanning Arrays",
        acronym="SA",
        tier=TIER_5,
        colour=Palette.ORANGE,
        volume=38,
        storage="Container",
        price_min=842,
        price_avg=1053,
        price_max=1264,
        recipes=[
            Recipe(
                time=600,
                amount=36,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("refined_metals", 100),
                    RecipeInput("silicon_wafers", 60),
                ),
            ),
            Recipe(
                time=600,
                amount=36,
                method="Teladi",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("silicon_wafers", 60),
                    RecipeInput("teladianium", 73),
                ),
            ),
        ],
    ),
    Ware(
        key="claytronics",
        name="Claytronics",
        acronym="Cl",
        tier=TIER_5,
        colour=Palette.BLUE,
        volume=24,
        storage="Container",
        price_min=1734,
        price_avg=2040,
        price_max=2346,
        recipes=[
            Recipe(
                time=900,
                amount=108,
                method="Universal",
                inputs=(
                    RecipeInput("antimatter_cells", 100),
                    RecipeInput("energy_cells", 140),
                    RecipeInput("microchips", 160),
                    RecipeInput("quantum_tubes", 100),
                ),
            ),
            Recipe(
                time=300,
                amount=60,
                method="Recycling",
                inputs=(
                    RecipeInput("energy_cells", 12000),
                    RecipeInput("scrap_metal", 300),
                ),
            ),
        ],
    ),
    Ware(
        key="advanced_electronics",
        name="Advanced Electronics",
        acronym="AE",
        tier=TIER_5,
        colour=Palette.TEAL,
        volume=30,
        storage="Container",
        price_min=710,
        price_avg=1014,
        price_max=1318,
        recipes=[
            Recipe(
                time=720,
                amount=54,
                method="Universal",
                inputs=(
                    RecipeInput("energy_cells", 60),
                    RecipeInput("microchips", 44),
                    RecipeInput("quantum_tubes", 20),
                ),
            )
        ],
    ),
)

WARES_TIER_6 = (
    Ware(
        key="ship_hulls",
        name="Ship Hulls",
        acronym="SH",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(RecipeInput("hull_parts", None),),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("metallic_microlattice", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="nav_beacons",
        name="Nav Beacons",
        acronym="NB",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(RecipeInput("hull_parts", None),),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="missiles",
        name="Missiles",
        acronym="Mi",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("missile_components", None),
                    RecipeInput("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="station_modules",
        name="Station modules",
        acronym="SM",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("hull_parts", None),
                    RecipeInput("claytronics", None),
                ),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("silicon_carbide", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="engines",
        name="Engines",
        acronym="En",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("antimatter_converters", None),
                    RecipeInput("engine_parts", None),
                ),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("metallic_microlattice", None),
                    RecipeInput("silicon_carbide", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="thrusters",
        name="Thrusters",
        acronym="Th",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("antimatter_converters", None),
                    RecipeInput("engine_parts", None),
                ),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("metallic_microlattice", None),
                    RecipeInput("silicon_carbide", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="mines",
        name="Mines",
        acronym="Mi",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("weapon_components", None),
                    RecipeInput("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="drones",
        name="Drones",
        acronym="Dr",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("drone_components", None),
                    RecipeInput("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="laser_towers",
        name="Laser Towers",
        acronym="LT",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("drone_components", None),
                    RecipeInput("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="shields",
        name="Shields",
        acronym="Sh",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("field_coils", None),
                    RecipeInput("shield_components", None),
                ),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("metallic_microlattice", None),
                    RecipeInput("silicon_carbide", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="turrets",
        name="Turrets",
        acronym="Tu",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("turret_components", None),
                    RecipeInput("advanced_electronics", None),
                ),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("metallic_microlattice", None),
                    RecipeInput("silicon_carbide", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="guns_and_launchers",
        name="Guns and Launchers",
        acronym="GL",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("advanced_electronics", None),
                    RecipeInput("weapon_components", None),
                ),
            ),
            Recipe(
                method="Terran",
                inputs=(
                    RecipeInput("metallic_microlattice", None),
                    RecipeInput("silicon_carbide", None),
                    RecipeInput("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="satellites",
        name="Satellites",
        acronym="Sa",
        tier=TIER_6,
        colour=TIER_6.colour,
        recipes=[
            Recipe(
                method="Universal",
                inputs=(
                    RecipeInput("scanning_arrays", None),
                    RecipeInput("advanced_electronics", None),
                    RecipeInput("hull_parts", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
)

WARES = (
    *WARES_TIER_0,
    *WARES_TIER_1,
    *WARES_TIER_2,
    *WARES_TIER_3,
    *WARES_TIER_4,
    *WARES_TIER_5,
    *WARES_TIER_6,
)
