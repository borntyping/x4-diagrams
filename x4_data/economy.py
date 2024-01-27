import typing

from x4.types import InputWare, Method, Recipe, Tier, Ware

COMMONWEALTH: typing.Sequence[Method] = (
    "Universal",
    "Argon",
    "Boron",
    "Paranid",
    "Split",
    "Teladi",
)

TIER_0 = Tier(key=0, name="Harvested")
TIER_1 = Tier(key=1, name="Basic Food")
TIER_2 = Tier(key=2, name="Food and Drugs")
TIER_3 = Tier(key=3, name="Refined")
TIER_4 = Tier(key=4, name="Advanced")
TIER_5 = Tier(key=5, name="Components")
TIER_6 = Tier(key=6, name="Equipment")

WARES_TIER_0 = (
    Ware(
        key="helium",
        name="Helium",
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
        tier=TIER_0,
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
                input_wares=(
                    InputWare("energy_cells", 10),
                    InputWare("raw_scrap", 1),
                ),
            )
        ],
    ),
    Ware(
        key="water",
        name="Water",
        tier=TIER_0,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("ice", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="energy_cells",
        name="Energy Cells",
        tier=TIER_0,
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
                input_wares=(),
            ),
            Recipe(
                time=60,
                amount=50,
                method="Terran",
                input_wares=(),
            ),
        ],
    ),
)

WARES_TIER_1 = (
    Ware(
        key="maja_snails",
        name="Maja Snails",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("water", 100),
                ),
            ),
        ],
    ),
    Ware(
        key="meat",
        name="Meat",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("water", 100),
                ),
            ),
        ],
    ),
    Ware(
        key="soja_beans",
        name="Soja Beans",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 30),
                    InputWare("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="spices",
        name="Spices",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="sunrise_flowers",
        name="Sunrise Flowers",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 30),
                    InputWare("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="swamp_plant",
        name="Swamp Plant",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("water", 100),
                ),
            ),
        ],
    ),
    Ware(
        key="wheat",
        name="Wheat",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="chelt_meat",
        name="Chelt Meat",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 50),
                    InputWare("water", 120),
                ),
            ),
        ],
    ),
    Ware(
        key="scruffin_fruits",
        name="Scruffin Fruit",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 30),
                    InputWare("water", 80),
                ),
            ),
        ],
    ),
    Ware(
        key="protein_paste",
        name="Protein Paste",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("ice", 80),
                    InputWare("methane", 200),
                ),
            )
        ],
    ),
    Ware(
        key="plankton",
        name="Plankton",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 20),
                    InputWare("water", 50),
                ),
            ),
        ],
    ),
    Ware(
        key="bogas",
        name="BoGas",
        tier=TIER_1,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("water", 100),
                ),
            ),
        ],
    ),
)

WARES_TIER_2 = (
    Ware(
        key="spacefuel",
        name="Spacefuel",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("water", 100),
                    InputWare("wheat", 80),
                ),
            )
        ],
    ),
    Ware(
        key="food_rations",
        name="Food Rations",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("meat", 40),
                    InputWare("spices", 40),
                    InputWare("wheat", 40),
                ),
            )
        ],
    ),
    Ware(
        key="maja_dust",
        name="Maja Dust",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("maja_snails", 120),
                    InputWare("spices", 60),
                ),
            )
        ],
    ),
    Ware(
        key="soja_husk",
        name="Soja Husk",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("maja_snails", 50),
                    InputWare("soja_beans", 40),
                    InputWare("spices", 20),
                ),
            )
        ],
    ),
    Ware(
        key="spaceweed",
        name="Spaceweed",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 140),
                    InputWare("spices", 40),
                    InputWare("swamp_plant", 120),
                ),
            )
        ],
    ),
    Ware(
        key="nostrop_oil",
        name="Nostrop Oil",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("spices", 40),
                    InputWare("sunrise_flowers", 40),
                    InputWare("water", 60),
                ),
            )
        ],
    ),
    Ware(
        key="medical_supplies",
        name="Medical Supplies",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("spices", 40),
                    InputWare("water", 60),
                    InputWare("wheat", 30),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Paranid",
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("soja_beans", 10),
                    InputWare("spices", 40),
                    InputWare("water", 60),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Teladi",
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("spices", 40),
                    InputWare("sunrise_flowers", 12),
                    InputWare("water", 60),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Split",
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("scruffin_fruits", 30),
                    InputWare("spices", 60),
                    InputWare("water", 60),
                ),
            ),
            Recipe(
                time=300,
                amount=140,
                method="Terran",
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("ice", 50),
                    InputWare("protein_paste", 24),
                ),
            ),
            Recipe(
                time=300,
                amount=208,
                method="Boron",
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("plankton", 95),
                    InputWare("water", 60),
                ),
            ),
        ],
    ),
    Ware(
        key="terran_mre",
        name="Terran MRE",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("protein_paste", 60),
                ),
            )
        ],
    ),
    Ware(
        key="stimulants",
        name="Stimulants",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("helium", 400),
                    InputWare("silicon", 20),
                ),
            )
        ],
    ),
    Ware(
        key="bofu",
        name="BoFu",
        tier=TIER_2,
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
                input_wares=(
                    InputWare("bogas", 40),
                    InputWare("energy_cells", 40),
                    InputWare("plankton", 120),
                ),
            )
        ],
    ),
)

WARES_TIER_3 = (
    Ware(
        key="superfluid_coolant",
        name="Superfluid Coolant",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("helium", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="graphene",
        name="Graphene",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("methane", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="refined_metals",
        name="Refined Metals",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 90),
                    InputWare("ore", 240),
                ),
            ),
        ],
    ),
    Ware(
        key="teladianium",
        name="Teladianium",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 45),
                    InputWare("ore", 280),
                ),
            ),
        ],
    ),
    Ware(
        key="antimatter_cells",
        name="Antimatter Cells",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 100),
                    InputWare("hydrogen", 320),
                ),
            ),
        ],
    ),
    Ware(
        key="silicon_wafers",
        name="Silicon Wafers",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 90),
                    InputWare("silicon", 240),
                ),
            ),
        ],
    ),
    Ware(
        key="computronic_substrate",
        name="Computronic Substrate",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 4000),
                    InputWare("hydrogen", 2000),
                    InputWare("ore", 3000),
                    InputWare("silicon", 3000),
                ),
            ),
            Recipe(
                time=300,
                amount=50,
                method="Recycling",
                input_wares=(
                    InputWare("energy_cells", 12500),
                    InputWare("scrap_metal", 1000),
                ),
            ),
        ],
    ),
    Ware(
        key="metallic_microlattice",
        name="Metallic Microlattice",
        tier=TIER_3,
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
                input_wares=(
                    InputWare("energy_cells", 50),
                    InputWare("helium", 130),
                    InputWare("ore", 50),
                ),
            )
        ],
    ),
)

WARES_TIER_4 = (
    Ware(
        key="plasma_conductors",
        name="Plasma Conductors",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("graphene", 96),
                    InputWare("superfluid_coolant", 140),
                ),
            )
        ],
    ),
    Ware(
        key="quantum_tubes",
        name="Quantum Tubes",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 40),
                    InputWare("graphene", 116),
                    InputWare("superfluid_coolant", 30),
                ),
            )
        ],
    ),
    Ware(
        key="advanced_composites",
        name="Advanced Composites",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 50),
                    InputWare("graphene", 80),
                    InputWare("refined_metals", 80),
                ),
            ),
            Recipe(
                time=300,
                amount=54,
                method="Teladi",
                input_wares=(
                    InputWare("energy_cells", 50),
                    InputWare("graphene", 80),
                    InputWare("teladianium", 58),
                ),
            ),
        ],
    ),
    Ware(
        key="hull_parts",
        name="Hull Parts",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("graphene", 40),
                    InputWare("refined_metals", 280),
                ),
            ),
            Recipe(
                time=300,
                amount=200,
                method="Recycling",
                input_wares=(
                    InputWare("energy_cells", 3500),
                    InputWare("scrap_metal", 75),
                ),
            ),
            Recipe(
                time=900,
                amount=294,
                method="Teladi",
                input_wares=(
                    InputWare("energy_cells", 80),
                    InputWare("graphene", 40),
                    InputWare("teladianium", 204),
                ),
            ),
        ],
    ),
    Ware(
        key="engine_parts",
        name="Engine Parts",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("antimatter_cells", 80),
                    InputWare("energy_cells", 60),
                    InputWare("refined_metals", 96),
                ),
            ),
            Recipe(
                time=900,
                amount=208,
                method="Teladi",
                input_wares=(
                    InputWare("antimatter_cells", 80),
                    InputWare("energy_cells", 60),
                    InputWare("teladianium", 70),
                ),
            ),
        ],
    ),
    Ware(
        key="microchips",
        name="Microchips",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 50),
                    InputWare("silicon_wafers", 200),
                ),
            )
        ],
    ),
    Ware(
        key="smart_chips",
        name="Smart Chips",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 50),
                    InputWare("silicon_wafers", 20),
                ),
            )
        ],
    ),
    Ware(
        key="silicon_carbide",
        name="Silicon Carbide",
        tier=TIER_4,
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
                input_wares=(
                    InputWare("energy_cells", 200),
                    InputWare("metallic_microlattice", 2),
                    InputWare("methane", 400),
                    InputWare("silicon", 300),
                ),
            ),
            Recipe(
                time=300,
                amount=60,
                method="Recycling",
                input_wares=(
                    InputWare("energy_cells", 4000),
                    InputWare("scrap_metal", 250),
                ),
            ),
        ],
    ),
)

WARES_TIER_5 = (
    Ware(
        key="drone_components",
        name="Drone Components",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("engine_parts", 20),
                    InputWare("hull_parts", 20),
                    InputWare("microchips", 20),
                    InputWare("scanning_arrays", 40),
                ),
            )
        ],
    ),
    Ware(
        key="turret_components",
        name="Turret Components",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("microchips", 20),
                    InputWare("quantum_tubes", 20),
                    InputWare("scanning_arrays", 10),
                ),
            )
        ],
    ),
    Ware(
        key="missile_components",
        name="Missile Components",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("advanced_composites", 2),
                    InputWare("energy_cells", 20),
                    InputWare("hull_parts", 2),
                ),
            )
        ],
    ),
    Ware(
        key="field_coils",
        name="Field Coils",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("plasma_conductors", 40),
                    InputWare("quantum_tubes", 43),
                ),
            )
        ],
    ),
    Ware(
        key="shield_components",
        name="Shield Components",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 70),
                    InputWare("plasma_conductors", 20),
                    InputWare("quantum_tubes", 20),
                ),
            )
        ],
    ),
    Ware(
        key="antimatter_converters",
        name="Antimatter Converters",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("advanced_composites", 20),
                    InputWare("energy_cells", 80),
                    InputWare("microchips", 30),
                ),
            )
        ],
    ),
    Ware(
        key="weapon_components",
        name="Weapon Components",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("hull_parts", 20),
                    InputWare("plasma_conductors", 30),
                ),
            )
        ],
    ),
    Ware(
        key="scanning_arrays",
        name="Scanning Arrays",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("refined_metals", 100),
                    InputWare("silicon_wafers", 60),
                ),
            ),
            Recipe(
                time=600,
                amount=36,
                method="Teladi",
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("silicon_wafers", 60),
                    InputWare("teladianium", 73),
                ),
            ),
        ],
        colour="orange1",
    ),
    Ware(
        key="claytronics",
        name="Claytronics",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("antimatter_cells", 100),
                    InputWare("energy_cells", 140),
                    InputWare("microchips", 160),
                    InputWare("quantum_tubes", 100),
                ),
            ),
            Recipe(
                time=300,
                amount=60,
                method="Recycling",
                input_wares=(
                    InputWare("energy_cells", 12000),
                    InputWare("scrap_metal", 300),
                ),
            ),
        ],
    ),
    Ware(
        key="advanced_electronics",
        name="Advanced Electronics",
        tier=TIER_5,
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
                input_wares=(
                    InputWare("energy_cells", 60),
                    InputWare("microchips", 44),
                    InputWare("quantum_tubes", 20),
                ),
            )
        ],
    ),
)

WARES_TIER_6 = (
    Ware(
        key="ship_hulls",
        name="Ship Hulls",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(InputWare("hull_parts", None),),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("metallic_microlattice", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="nav_beacons",
        name="Nav Beacons",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(InputWare("hull_parts", None),),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="missiles",
        name="Missiles",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("missile_components", None),
                    InputWare("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="station_modules",
        name="Station modules",
        tier=TIER_6,
        colour="hotpink1",
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("hull_parts", None),
                    InputWare("claytronics", None),
                ),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("silicon_carbide", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="engines",
        name="Engines",
        tier=TIER_6,
        colour="hotpink1",
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("antimatter_converters", None),
                    InputWare("engine_parts", None),
                ),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("metallic_microlattice", None),
                    InputWare("silicon_carbide", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="thrusters",
        name="Thrusters",
        tier=TIER_6,
        colour="hotpink1",
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("antimatter_converters", None),
                    InputWare("engine_parts", None),
                ),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("metallic_microlattice", None),
                    InputWare("silicon_carbide", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="mines",
        name="Mines",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("weapon_components", None),
                    InputWare("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="drones",
        name="Drones",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("drone_components", None),
                    InputWare("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="laser_towers",
        name="Laser Towers",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("drone_components", None),
                    InputWare("smart_chips", None),
                ),
            )
        ],
        tags={"terminal"},
    ),
    Ware(
        key="shields",
        name="Shields",
        tier=TIER_6,
        colour="hotpink1",
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("field_coils", None),
                    InputWare("shield_components", None),
                ),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("metallic_microlattice", None),
                    InputWare("silicon_carbide", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="turrets",
        name="Turrets",
        tier=TIER_6,
        colour="hotpink1",
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("turret_components", None),
                    InputWare("advanced_electronics", None),
                ),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("metallic_microlattice", None),
                    InputWare("silicon_carbide", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="guns_and_launchers",
        name="Guns and Launchers",
        tier=TIER_6,
        colour="hotpink1",
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("advanced_electronics", None),
                    InputWare("weapon_components", None),
                ),
            ),
            Recipe(
                method="Terran",
                input_wares=(
                    InputWare("metallic_microlattice", None),
                    InputWare("silicon_carbide", None),
                    InputWare("computronic_substrate", None),
                ),
            ),
        ],
        tags={"terminal"},
    ),
    Ware(
        key="satellites",
        name="Satellites",
        tier=TIER_6,
        recipes=[
            Recipe(
                method="Universal",
                input_wares=(
                    InputWare("scanning_arrays", None),
                    InputWare("advanced_electronics", None),
                    InputWare("hull_parts", None),
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
