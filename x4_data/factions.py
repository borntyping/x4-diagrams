from x4.types import Faction
from x4_data.races import ARGON, KHAAK, PARANID, SPLIT, TELADI, TERRAN, XENON

ALI = Faction(
    tag="ALI",
    race=PARANID,
    name="Alliance of the Word",
    allies=["PAR"],
    enemies=[],
    hostiles=["KHK", "XEN", "YAK"],
)
ANT = Faction(
    tag="ANT",
    race=ARGON,
    name="Antigone Republic",
    allies=["ARG"],
    enemies=["DUC", "FAF", "FRF", "HOP", "SCA", "TER", "VIG", "ZYA"],
    hostiles=["KHK", "XEN", "YAK"],
)
ARG = Faction(
    tag="ARG",
    race=ARGON,
    name="Argon Federation",
    allies=["ANT"],
    enemies=["DUC", "FRF", "HOP", "TER", "VIG", "ZYA"],
    hostiles=["FAF", "SCA", "KHK", "XEN", "YAK"],
)
DUC = Faction(
    tag="DUC",
    race=PARANID,
    name="Duke's Bucaneers",
    allies=[],
    enemies=["ANT", "ARG", "FRF", "PAR", "HAT", "HOP", "MIN", "RIP", "PIO", "TER", "YOU", "VIG", "ZYA"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
FAF = Faction(
    tag="FAF",
    race=SPLIT,
    name="Fallen Families",
    allies=[],
    enemies=["ANT", "TEL"],
    hostiles=["ARG", "DUC", "PAR", "HOP", "KHK", "MIN", "RIP", "PIO", "TER", "VIG", "XEN", "YAK", "ZYA"],
)
FRF = Faction(
    tag="FRF",
    race=SPLIT,
    name="Free Families",
    allies=[],
    enemies=["ANT", "ARG", "DUC", "SCA", "TER", "VIG"],
    hostiles=["KHK", "XEN", "YAK"],
)
PAR = Faction(
    tag="PAR",
    race=PARANID,
    name="Godrealm of the Paranid",
    allies=["ALI"],
    enemies=["DUC", "HOP", "TER", "VIG"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
HAT = Faction(
    tag="HAT",
    race=ARGON,
    name="Hatikvah Free League",
    allies=[],
    enemies=["DUC"],
    hostiles=["KHK", "XEN", "YAK"],
)
HOP = Faction(
    tag="HOP",
    race=PARANID,
    name="Holy Order of the Pontifex",
    allies=[],
    enemies=["ANT", "ARG", "DUC", "PAR", "MIN", "TEL", "TER", "VIG"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
KHK = Faction(
    tag="KHK",
    race=KHAAK,
    name="Kha'ak",
    allies=[],
    enemies=[],
    hostiles=[
        "ALI",
        "ANT",
        "ARG",
        "DUC",
        "FAF",
        "FRF",
        "PAR",
        "HAT",
        "HOP",
        "MIN",
        "RIP",
        "SCA",
        "PIO",
        "TEL",
        "TER",
        "YOU",
        "VIG",
        "XEN",
        "YAK",
        "ZYA",
    ],
)
MIN = Faction(
    tag="MIN",
    race=TELADI,
    name="Ministry of Finance",
    allies=["TEL"],
    enemies=["DUC", "HOP", "TER", "VIG"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
RIP = Faction(
    tag="RIP",
    race=ARGON,
    name="Riptide Rakers",
    allies=[],
    enemies=["DUC", "TER"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
SCA = Faction(
    tag="SCA",
    race=TELADI,
    name="Scale Plate Pact",
    allies=[],
    enemies=["ANT", "FRF"],
    hostiles=["ARG", "DUC", "PAR", "HOP", "KHK", "MIN", "RIP", "PIO", "TER", "VIG", "XEN", "YAK", "ZYA"],
)
PIO = Faction(
    tag="PIO",
    race=TERRAN,
    name="Segaris Pioneers",
    allies=[],
    enemies=["DUC", "VIG", "YAK"],
    hostiles=["FAF", "KHK", "SCA", "XEN"],
)
TEL = Faction(
    tag="TEL",
    race=TELADI,
    name="Teladi Company",
    allies=["MIN"],
    enemies=["FAF", "HOP"],
    hostiles=["KHK", "XEN", "YAK"],
)
TER = Faction(
    tag="TER",
    race=TERRAN,
    name="Terran Protectorate",
    allies=[],
    enemies=["ANT", "ARG", "DUC", "FRF", "PAR", "MIN", "RIP", "VIG", "ZYA"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
VIG = Faction(
    tag="VIG",
    race=ARGON,
    name="Vigor Syndicate",
    allies=[],
    enemies=["ANT", "ARG", "DUC", "FRF", "PAR", "HOP", "MIN", "PIO", "TER", "ZYA"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)
XEN = Faction(
    tag="XEN",
    race=XENON,
    name="Xenon",
    allies=[],
    enemies=["YAK"],
    hostiles=[
        "ALI",
        "ANT",
        "ARG",
        "DUC",
        "FAF",
        "FRF",
        "PAR",
        "HAT",
        "HOP",
        "MIN",
        "RIP",
        "SCA",
        "PIO",
        "TEL",
        "TER",
        "YOU",
        "VIG",
        "ZYA",
    ],
)
YAK = Faction(
    tag="YAK",
    race=ARGON,
    name="Yaki",
    allies=[],
    enemies=["PIO", "XEN"],
    hostiles=[
        "ALI",
        "ANT",
        "ARG",
        "DUC",
        "FAF",
        "FRF",
        "PAR",
        "HAT",
        "HOP",
        "KHK",
        "MIN",
        "RIP",
        "SCA",
        "TEL",
        "TER",
        "YOU",
        "VIG",
        "ZYA",
    ],
)
ZYA = Faction(
    tag="ZYA",
    race=SPLIT,
    name="Zyarth Patriarchy",
    allies=[],
    enemies=["ANT", "ARG", "DUC", "TER", "YOU", "VIG"],
    hostiles=["FAF", "KHK", "SCA", "XEN", "YAK"],
)

FACTIONS = [ALI, ANT, ARG, DUC, FAF, FRF, PAR, HAT, HOP, KHK, MIN, RIP, SCA, PIO, TEL, TER, VIG, XEN, YAK, ZYA]

ALIENS = [KHK, XEN, YAK]
PIRATES = [DUC, FAF, SCA, VIG]
