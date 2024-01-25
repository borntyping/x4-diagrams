from x4.types import Production, Ware, Tier

UNDEFINED = 10

TIERS = [
    Tier(
        level=0,
        name="Harvested",
        wares=[
            Ware(
                key="helium",
                name="Helium",
                volume=6,
                storage="Liquid",
                price_min=37,
                price_avg=44,
                price_max=51,
                production=[],
            ),
            Ware(
                key="methane",
                name="Methane",
                volume=6,
                storage="Liquid",
                price_min=41,
                price_avg=48,
                price_max=55,
                production=[],
            ),
            Ware(
                key="ore",
                name="Ore",
                volume=10,
                storage="Solid",
                price_min=43,
                price_avg=50,
                price_max=58,
                production=[],
            ),
            Ware(
                key="hydrogen",
                name="Hydrogen",
                volume=6,
                storage="Liquid",
                price_min=49,
                price_avg=58,
                price_max=67,
                production=[],
            ),
            Ware(
                key="silicon",
                name="Silicon",
                volume=10,
                storage="Solid",
                price_min=111,
                price_avg=130,
                price_max=150,
                production=[],
            ),
            Ware(
                key="nividium",
                name="Nividium",
                volume=10,
                storage="Solid",
                price_min=434,
                price_avg=510,
                price_max=587,
                production=[],
            ),
            Ware(
                key="ice",
                name="Ice",
                volume=8,
                storage="Solid",
                price_min=26,
                price_avg=30,
                price_max=35,
                production=[],
            ),
            Ware(
                key="raw_scrap",
                name="Raw Scrap",
                volume=10,
                storage="Solid",
                price_min=153,
                price_avg=180,
                price_max=207,
                production=[],
            ),
            Ware(
                key="scrap_metal",
                name="Scrap Metal",
                volume=10,
                storage="Solid",
                price_min=318,
                price_avg=375,
                price_max=431,
                production=[
                    Production(
                        time=60,
                        amount=1,
                        method="Recycling",
                        wares={
                            "energy_cells": 10,
                            "raw_scrap": 1,
                        },
                    ),
                ],
            ),
            Ware(
                key="water",
                name="Water",
                volume=6,
                storage="Container",
                price_min=32,
                price_avg=53,
                price_max=74,
                production=[
                    Production(
                        time=120,
                        amount=193,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "ice": 320,
                        },
                    ),
                ],
            ),
            Ware(
                key="energy_cells",
                name="Energy Cells",
                volume=1,
                storage="Container",
                price_min=10,
                price_avg=16,
                price_max=22,
                production=[
                    Production(
                        time=60,
                        amount=175,
                        method="Universal",
                        wares={},
                    ),
                    Production(
                        time=60,
                        amount=50,
                        method="Terran",
                        wares={},
                    ),
                ],
            ),
        ],
    ),
    Tier(
        level=1,
        name="Basic Food",
        wares=[
            Ware(
                key="maja_snails",
                name="Maja Snails",
                volume=6,
                storage="Container",
                price_min=35,
                price_avg=58,
                price_max=81,
                production=[
                    Production(
                        time=450,
                        amount=146,
                        method="Paranid",
                        wares={
                            "energy_cells": 40,
                            "water": 100,
                        },
                    ),
                ],
            ),
            Ware(
                key="meat",
                name="Meat",
                volume=6,
                storage="Container",
                price_min=29,
                price_avg=48,
                price_max=68,
                production=[
                    Production(
                        time=450,
                        amount=290,
                        method="Argon",
                        wares={
                            "energy_cells": 80,
                            "water": 100,
                        },
                    ),
                ],
            ),
            Ware(
                key="soja_beans",
                name="Soja Beans",
                volume=5,
                storage="Container",
                price_min=40,
                price_avg=67,
                price_max=93,
                production=[
                    Production(
                        time=300,
                        amount=104,
                        method="Paranid",
                        wares={
                            "energy_cells": 30,
                            "water": 80,
                        },
                    ),
                ],
            ),
            Ware(
                key="spices",
                name="Spices",
                volume=3,
                storage="Container",
                price_min=12,
                price_avg=20,
                price_max=28,
                production=[
                    Production(
                        time=600,
                        amount=500,
                        method="Universal",
                        wares={
                            "energy_cells": 40,
                            "water": 80,
                        },
                    ),
                ],
            ),
            Ware(
                key="sunrise_flowers",
                name="Sunrise Flowers",
                volume=5,
                storage="Container",
                price_min=48,
                price_avg=80,
                price_max=112,
                production=[
                    Production(
                        time=300,
                        amount=100,
                        method="Teladi",
                        wares={
                            "energy_cells": 30,
                            "water": 80,
                        },
                    ),
                ],
            ),
            Ware(
                key="swamp_plant",
                name="Swamp Plant",
                volume=6,
                storage="Container",
                price_min=50,
                price_avg=84,
                price_max=117,
                production=[
                    Production(
                        time=450,
                        amount=120,
                        method="Teladi",
                        wares={
                            "energy_cells": 40,
                            "water": 100,
                        },
                    ),
                ],
            ),
            Ware(
                key="wheat",
                name="Wheat",
                volume=4,
                storage="Container",
                price_min=19,
                price_avg=31,
                price_max=44,
                production=[
                    Production(
                        time=300,
                        amount=310,
                        method="Argon",
                        wares={
                            "energy_cells": 60,
                            "water": 80,
                        },
                    ),
                ],
            ),
            Ware(
                key="chelt_meat",
                name="Chelt Meat",
                volume=7,
                storage="Container",
                price_min=31,
                price_avg=51,
                price_max=72,
                production=[
                    Production(
                        time=450,
                        amount=209,
                        method="Split",
                        wares={
                            "energy_cells": 50,
                            "water": 120,
                        },
                    ),
                ],
            ),
            Ware(
                key="scruffin_fruits",
                name="Scruffin Fruit",
                volume=6,
                storage="Container",
                price_min=17,
                price_avg=28,
                price_max=40,
                production=[
                    Production(
                        time=300,
                        amount=255,
                        method="Split",
                        wares={
                            "energy_cells": 30,
                            "water": 80,
                        },
                    ),
                ],
            ),
            Ware(
                key="protein_paste",
                name="Protein Paste",
                volume=4,
                storage="Container",
                price_min=57,
                price_avg=96,
                price_max=134,
                production=[
                    Production(
                        time=300,
                        amount=219,
                        method="Terran",
                        wares={
                            "energy_cells": 80,
                            "ice": 80,
                            "methane": 200,
                        },
                    )
                ],
            ),
            Ware(
                key="plankton",
                name="Plankton",
                volume=1,
                storage="Container",
                price_min=11,
                price_avg=18,
                price_max=25,
                production=[
                    Production(
                        time=400,
                        amount=275,
                        method="Boron",
                        wares={
                            "energy_cells": 20,
                            "water": 50,
                        },
                    ),
                ],
            ),
            Ware(
                key="bogas",
                name="BoGas",
                volume=4,
                storage="Container",
                price_min=44,
                price_avg=73,
                price_max=102,
                production=[
                    Production(
                        time=150,
                        amount=110,
                        method="Boron",
                        wares={
                            "energy_cells": 40,
                            "water": 100,
                        },
                    ),
                ],
            ),
        ],
    ),
    Tier(
        level=2,
        name="Food and Drugs",
        wares=[
            Ware(
                key="spacefuel",
                name="Spacefuel",
                volume=2,
                storage="Container",
                price_min=60,
                price_avg=133,
                price_max=207,
                production=[
                    Production(
                        time=480,
                        amount=98,
                        method="Argon",
                        wares={
                            "energy_cells": 40,
                            "water": 100,
                            "wheat": 80,
                        },
                    )
                ],
            ),
            Ware(
                key="food_rations",
                name="Food Rations",
                volume=1,
                storage="Container",
                price_min=12,
                price_avg=21,
                price_max=29,
                production=[
                    Production(
                        time=240,
                        amount=460,
                        method="Argon",
                        wares={
                            "energy_cells": 100,
                            "meat": 40,
                            "spices": 40,
                            "wheat": 40,
                        },
                    )
                ],
            ),
            Ware(
                key="maja_dust",
                name="Maja Dust",
                volume=6,
                storage="Container",
                price_min=94,
                price_avg=208,
                price_max=323,
                production=[
                    Production(
                        time=600,
                        amount=64,
                        method="Paranid",
                        wares={
                            "energy_cells": 40,
                            "maja_snails": 120,
                            "spices": 60,
                        },
                    )
                ],
            ),
            Ware(
                key="soja_husk",
                name="Soja Husk",
                volume=1,
                storage="Container",
                price_min=19,
                price_avg=32,
                price_max=45,
                production=[
                    Production(
                        time=300,
                        amount=350,
                        method="Paranid",
                        wares={
                            "energy_cells": 80,
                            "maja_snails": 50,
                            "soja_beans": 40,
                            "spices": 20,
                        },
                    )
                ],
            ),
            Ware(
                key="spaceweed",
                name="Spaceweed",
                volume=3,
                storage="Container",
                price_min=75,
                price_avg=166,
                price_max=257,
                production=[
                    Production(
                        time=600,
                        amount=183,
                        method="Teladi",
                        wares={
                            "energy_cells": 140,
                            "spices": 40,
                            "swamp_plant": 120,
                        },
                    )
                ],
            ),
            Ware(
                key="nostrop_oil",
                name="Nostrop Oil",
                volume=1,
                storage="Container",
                price_min=20,
                price_avg=34,
                price_max=47,
                production=[
                    Production(
                        time=300,
                        amount=500,
                        method="Teladi",
                        wares={
                            "energy_cells": 100,
                            "spices": 40,
                            "sunrise_flowers": 40,
                            "water": 60,
                        },
                    )
                ],
            ),
            Ware(
                key="medical_supplies",
                name="Medical Supplies",
                volume=2,
                storage="Container",
                price_min=43,
                price_avg=66,
                price_max=89,
                production=[
                    Production(
                        time=300,
                        amount=208,
                        method="Argon",
                        wares={
                            "energy_cells": 100,
                            "spices": 40,
                            "water": 60,
                            "wheat": 30,
                        },
                    ),
                    Production(
                        time=300,
                        amount=208,
                        method="Paranid",
                        wares={
                            "energy_cells": 100,
                            "soja_beans": 10,
                            "spices": 40,
                            "water": 60,
                        },
                    ),
                    Production(
                        time=300,
                        amount=208,
                        method="Teladi",
                        wares={
                            "energy_cells": 100,
                            "spices": 40,
                            "sunrise_flowers": 12,
                            "water": 60,
                        },
                    ),
                    Production(
                        time=300,
                        amount=208,
                        method="Split",
                        wares={
                            "energy_cells": 100,
                            "scruffin_fruits": 30,
                            "spices": 60,
                            "water": 60,
                        },
                    ),
                    Production(
                        time=300,
                        amount=140,
                        method="Terran",
                        wares={
                            "energy_cells": 100,
                            "ice": 50,
                            "protein_paste": 24,
                        },
                    ),
                    Production(
                        time=300,
                        amount=208,
                        method="Boron",
                        wares={
                            "energy_cells": 100,
                            "plankton": 95,
                            "water": 60,
                        },
                    ),
                ],
            ),
            Ware(
                key="terran_mre",
                name="Terran MRE",
                volume=2,
                storage="Container",
                price_min=32,
                price_avg=54,
                price_max=75,
                production=[
                    Production(
                        time=240,
                        amount=175,
                        method="Terran",
                        wares={
                            "energy_cells": 60,
                            "protein_paste": 60,
                        },
                    )
                ],
            ),
            Ware(
                key="stimulants",
                name="Stimulants",
                volume=12,
                storage="Container",
                price_min=153,
                price_avg=340,
                price_max=527,
                production=[
                    Production(
                        time=300,
                        amount=98,
                        method="Terran",
                        wares={
                            "energy_cells": 80,
                            "helium": 400,
                            "silicon": 20,
                        },
                    )
                ],
            ),
            Ware(
                key="bofu",
                name="BoFu",
                volume=4,
                storage="Container",
                price_min=61,
                price_avg=101,
                price_max=142,
                production=[
                    Production(
                        time=240,
                        amount=82,
                        method="Boron",
                        wares={
                            "bogas": 40,
                            "energy_cells": 40,
                            "plankton": 120,
                        },
                    )
                ],
            ),
        ],
    ),
    Tier(
        level=3,
        name="Refined",
        wares=[
            Ware(
                key="superfluid_coolant",
                name="Superfluid Coolant",
                volume=16,
                storage="Container",
                price_min=90,
                price_avg=150,
                price_max=211,
                production=[
                    Production(
                        time=240,
                        amount=95,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "helium": 320,
                        },
                    ),
                ],
            ),
            Ware(
                key="graphene",
                name="Graphene",
                volume=20,
                storage="Container",
                price_min=100,
                price_avg=166,
                price_max=233,
                production=[
                    Production(
                        time=240,
                        amount=96,
                        method="Universal",
                        wares={
                            "energy_cells": 80,
                            "methane": 320,
                        },
                    ),
                ],
            ),
            Ware(
                key="refined_metals",
                name="Refined Metals",
                volume=14,
                storage="Container",
                price_min=89,
                price_avg=148,
                price_max=207,
                production=[
                    Production(
                        time=150,
                        amount=88,
                        method="Universal",
                        wares={
                            "energy_cells": 90,
                            "ore": 240,
                        },
                    ),
                ],
            ),
            Ware(
                key="teladianium",
                name="Teladianium",
                volume=16,
                storage="Container",
                price_min=121,
                price_avg=202,
                price_max=283,
                production=[
                    Production(
                        time=120,
                        amount=70,
                        method="Teladi",
                        wares={
                            "energy_cells": 45,
                            "ore": 280,
                        },
                    ),
                ],
            ),
            Ware(
                key="antimatter_cells",
                name="Antimatter Cells",
                volume=18,
                storage="Container",
                price_min=121,
                price_avg=202,
                price_max=282,
                production=[
                    Production(
                        time=120,
                        amount=99,
                        method="Universal",
                        wares={
                            "energy_cells": 100,
                            "hydrogen": 320,
                        },
                    ),
                ],
            ),
            Ware(
                key="silicon_wafers",
                name="Silicon Wafers",
                volume=18,
                storage="Container",
                price_min=180,
                price_avg=299,
                price_max=419,
                production=[
                    Production(
                        time=180,
                        amount=107,
                        method="Universal",
                        wares={
                            "energy_cells": 90,
                            "silicon": 240,
                        },
                    ),
                ],
            ),
            Ware(
                key="computronic_substrate",
                name="Computronic Substrate",
                volume=50,
                storage="Container",
                price_min=7452,
                price_avg=8280,
                price_max=9108,
                production=[
                    Production(
                        time=600,
                        amount=98,
                        method="Terran",
                        wares={
                            "energy_cells": 4000,
                            "hydrogen": 2000,
                            "ore": 3000,
                            "silicon": 3000,
                        },
                    ),
                    Production(
                        time=300,
                        amount=50,
                        method="Recycling",
                        wares={
                            "energy_cells": 12500,
                            "scrap_metal": 1000,
                        },
                    ),
                ],
            ),
            Ware(
                key="metallic_microlattice",
                name="Metallic Microlattice",
                volume=1,
                storage="Container",
                price_min=42,
                price_avg=50,
                price_max=57,
                production=[
                    Production(
                        time=180,
                        amount=190,
                        method="Terran",
                        wares={
                            "energy_cells": 50,
                            "helium": 130,
                            "ore": 50,
                        },
                    )
                ],
            ),
        ],
    ),
    Tier(
        level=4,
        name="Advanced",
        wares=[
            Ware(
                key="plasma_conductors",
                name="Plasma Conductors",
                volume=32,
                storage="Container",
                price_min=769,
                price_avg=1026,
                price_max=1282,
                production=[
                    Production(
                        time=900,
                        amount=44,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "graphene": 96,
                            "superfluid_coolant": 140,
                        },
                    )
                ],
            ),
            Ware(
                key="quantum_tubes",
                name="Quantum Tubes",
                volume=22,
                storage="Container",
                price_min=225,
                price_avg=300,
                price_max=375,
                production=[
                    Production(
                        time=720,
                        amount=94,
                        method="Universal",
                        wares={
                            "energy_cells": 40,
                            "graphene": 116,
                            "superfluid_coolant": 30,
                        },
                    )
                ],
            ),
            Ware(
                key="advanced_composites",
                name="Advanced Composites",
                volume=32,
                storage="Container",
                price_min=432,
                price_avg=540,
                price_max=648,
                production=[
                    Production(
                        time=300,
                        amount=54,
                        method="Universal",
                        wares={
                            "energy_cells": 50,
                            "graphene": 80,
                            "refined_metals": 80,
                        },
                    ),
                    Production(
                        time=300,
                        amount=54,
                        method="Teladi",
                        wares={
                            "energy_cells": 50,
                            "graphene": 80,
                            "teladianium": 58,
                        },
                    ),
                ],
            ),
            Ware(
                key="hull_parts",
                name="Hull Parts",
                volume=12,
                storage="Container",
                price_min=146,
                price_avg=209,
                price_max=272,
                production=[
                    Production(
                        time=900,
                        amount=294,
                        method="Universal",
                        wares={
                            "energy_cells": 80,
                            "graphene": 40,
                            "refined_metals": 280,
                        },
                    ),
                    Production(
                        time=300,
                        amount=200,
                        method="Recycling",
                        wares={
                            "energy_cells": 3500,
                            "scrap_metal": 75,
                        },
                    ),
                    Production(
                        time=900,
                        amount=294,
                        method="Teladi",
                        wares={
                            "energy_cells": 80,
                            "graphene": 40,
                            "teladianium": 204,
                        },
                    ),
                ],
            ),
            Ware(
                key="engine_parts",
                name="Engine Parts",
                volume=15,
                storage="Container",
                price_min=128,
                price_avg=182,
                price_max=237,
                production=[
                    Production(
                        time=900,
                        amount=208,
                        method="Universal",
                        wares={
                            "antimatter_cells": 80,
                            "energy_cells": 60,
                            "refined_metals": 96,
                        },
                    ),
                    Production(
                        time=900,
                        amount=208,
                        method="Teladi",
                        wares={
                            "antimatter_cells": 80,
                            "energy_cells": 60,
                            "teladianium": 70,
                        },
                    ),
                ],
            ),
            Ware(
                key="microchips",
                name="Microchips",
                volume=22,
                storage="Container",
                price_min=805,
                price_avg=948,
                price_max=1090,
                production=[
                    Production(
                        time=600,
                        amount=72,
                        method="Universal",
                        wares={
                            "energy_cells": 50,
                            "silicon_wafers": 200,
                        },
                    )
                ],
            ),
            Ware(
                key="smart_chips",
                name="Smart Chips",
                volume=2,
                storage="Container",
                price_min=46,
                price_avg=57,
                price_max=69,
                production=[
                    Production(
                        time=600,
                        amount=143,
                        method="Universal",
                        wares={
                            "energy_cells": 50,
                            "silicon_wafers": 20,
                        },
                    )
                ],
            ),
            Ware(
                key="silicon_carbide",
                name="Silicon Carbide",
                volume=20,
                storage="Container",
                price_min=1202,
                price_avg=1414,
                price_max=1627,
                production=[
                    Production(
                        time=300,
                        amount=48,
                        method="Terran",
                        wares={
                            "energy_cells": 200,
                            "metallic_microlattice": 2,
                            "methane": 400,
                            "silicon": 300,
                        },
                    ),
                    Production(
                        time=300,
                        amount=60,
                        method="Recycling",
                        wares={
                            "energy_cells": 4000,
                            "scrap_metal": 250,
                        },
                    ),
                ],
            ),
        ],
    ),
    Tier(
        level=5,
        name="Components",
        wares=[
            Ware(
                key="drone_components",
                name="Drone Components",
                volume=30,
                storage="Container",
                price_min=685,
                price_avg=914,
                price_max=1142,
                production=[
                    Production(
                        time=1200,
                        amount=105,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "engine_parts": 20,
                            "hull_parts": 20,
                            "microchips": 20,
                            "scanning_arrays": 40,
                        },
                    )
                ],
            ),
            Ware(
                key="turret_components",
                name="Turret Components",
                volume=20,
                storage="Container",
                price_min=164,
                price_avg=273,
                price_max=383,
                production=[
                    Production(
                        time=1800,
                        amount=170,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "microchips": 20,
                            "quantum_tubes": 20,
                            "scanning_arrays": 10,
                        },
                    )
                ],
            ),
            Ware(
                key="missile_components",
                name="Missile Components",
                volume=2,
                storage="Container",
                price_min=6,
                price_avg=9,
                price_max=13,
                production=[
                    Production(
                        time=900,
                        amount=281,
                        method="Universal",
                        wares={
                            "advanced_composites": 2,
                            "energy_cells": 20,
                            "hull_parts": 2,
                        },
                    )
                ],
            ),
            Ware(
                key="field_coils",
                name="Field Coils",
                volume=15,
                storage="Container",
                price_min=247,
                price_avg=412,
                price_max=576,
                production=[
                    Production(
                        time=600,
                        amount=175,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "plasma_conductors": 40,
                            "quantum_tubes": 43,
                        },
                    )
                ],
            ),
            Ware(
                key="shield_components",
                name="Shield Components",
                volume=10,
                storage="Container",
                price_min=113,
                price_avg=188,
                price_max=264,
                production=[
                    Production(
                        time=1200,
                        amount=193,
                        method="Universal",
                        wares={
                            "energy_cells": 70,
                            "plasma_conductors": 20,
                            "quantum_tubes": 20,
                        },
                    )
                ],
            ),
            Ware(
                key="antimatter_converters",
                name="Antimatter Converters",
                volume=10,
                storage="Container",
                price_min=248,
                price_avg=354,
                price_max=461,
                production=[
                    Production(
                        time=300,
                        amount=133,
                        method="Universal",
                        wares={
                            "advanced_composites": 20,
                            "energy_cells": 80,
                            "microchips": 30,
                        },
                    )
                ],
            ),
            Ware(
                key="weapon_components",
                name="Weapon Components",
                volume=20,
                storage="Container",
                price_min=171,
                price_avg=285,
                price_max=399,
                production=[
                    Production(
                        time=1800,
                        amount=170,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "hull_parts": 20,
                            "plasma_conductors": 30,
                        },
                    )
                ],
            ),
            Ware(
                key="scanning_arrays",
                name="Scanning Arrays",
                volume=38,
                storage="Container",
                price_min=842,
                price_avg=1053,
                price_max=1264,
                production=[
                    Production(
                        time=600,
                        amount=36,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "refined_metals": 100,
                            "silicon_wafers": 60,
                        },
                    ),
                    Production(
                        time=600,
                        amount=36,
                        method="Teladi",
                        wares={
                            "energy_cells": 60,
                            "silicon_wafers": 60,
                            "teladianium": 73,
                        },
                    ),
                ],
                colour="orange1",
            ),
            Ware(
                key="claytronics",
                name="Claytronics",
                volume=24,
                storage="Container",
                price_min=1734,
                price_avg=2040,
                price_max=2346,
                production=[
                    Production(
                        time=900,
                        amount=108,
                        method="Universal",
                        wares={
                            "antimatter_cells": 100,
                            "energy_cells": 140,
                            "microchips": 160,
                            "quantum_tubes": 100,
                        },
                    ),
                    Production(
                        time=300,
                        amount=60,
                        method="Recycling",
                        wares={
                            "energy_cells": 12000,
                            "scrap_metal": 300,
                        },
                    ),
                ],
            ),
            Ware(
                key="advanced_electronics",
                name="Advanced Electronics",
                volume=30,
                storage="Container",
                price_min=710,
                price_avg=1014,
                price_max=1318,
                production=[
                    Production(
                        time=720,
                        amount=54,
                        method="Universal",
                        wares={
                            "energy_cells": 60,
                            "microchips": 44,
                            "quantum_tubes": 20,
                        },
                    )
                ],
            ),
        ],
    ),
    Tier(
        level=6,
        name="Equipment",
        wares=[
            Ware(
                key="ship_hulls",
                name="Ship Hulls",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "hull_parts": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "metallic_microlattice": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="nav_beacons",
                name="Nav Beacons",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "hull_parts": UNDEFINED,
                        },
                    )
                ],
                tags={"terminal"},
            ),
            Ware(
                key="missiles",
                name="Missiles",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "missile_components": UNDEFINED,
                            "smart_chips": UNDEFINED,
                        },
                    )
                ],
                tags={"terminal"},
            ),
            Ware(
                key="station_modules",
                name="Station modules",
                colour="hotpink1",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "hull_parts": UNDEFINED,
                            "claytronics": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "silicon_carbide": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="engines",
                name="Engines",
                colour="hotpink1",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "antimatter_converters": UNDEFINED,
                            "engine_parts": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "metallic_microlattice": UNDEFINED,
                            "silicon_carbide": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="thrusters",
                name="Thrusters",
                colour="hotpink1",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "antimatter_converters": UNDEFINED,
                            "engine_parts": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "metallic_microlattice": UNDEFINED,
                            "silicon_carbide": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="mines",
                name="Mines",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "weapon_components": UNDEFINED,
                            "smart_chips": UNDEFINED,
                        },
                    )
                ],
                tags={"terminal"},
            ),
            Ware(
                key="drones",
                name="Drones",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "drone_components": UNDEFINED,
                            "smart_chips": UNDEFINED,
                        },
                    )
                ],
                tags={"terminal"},
            ),
            Ware(
                key="laser_towers",
                name="Laser Towers",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "drone_components": UNDEFINED,
                            "smart_chips": UNDEFINED,
                        },
                    )
                ],
                tags={"terminal"},
            ),
            Ware(
                key="shields",
                name="Shields",
                colour="hotpink1",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "field_coils": UNDEFINED,
                            "shield_components": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "metallic_microlattice": UNDEFINED,
                            "silicon_carbide": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="turrets",
                name="Turrets",
                colour="hotpink1",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "turret_components": UNDEFINED,
                            "advanced_electronics": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "metallic_microlattice": UNDEFINED,
                            "silicon_carbide": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="guns_and_launchers",
                name="Guns and Launchers",
                colour="hotpink1",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "advanced_electronics": UNDEFINED,
                            "weapon_components": UNDEFINED,
                        },
                    ),
                    Production(
                        method="Terran",
                        wares={
                            "metallic_microlattice": UNDEFINED,
                            "silicon_carbide": UNDEFINED,
                            "computronic_substrate": UNDEFINED,
                        },
                    ),
                ],
                tags={"terminal"},
            ),
            Ware(
                key="satellites",
                name="Satellites",
                production=[
                    Production(
                        method="Universal",
                        wares={
                            "scanning_arrays": UNDEFINED,
                            "advanced_electronics": UNDEFINED,
                            "hull_parts": UNDEFINED,
                        },
                    )
                ],
                tags={"terminal"},
            ),
        ],
    ),
]
