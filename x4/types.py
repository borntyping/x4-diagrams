import dataclasses
import typing

import structlog

logger = structlog.get_logger(logger_name=__name__)


Method = typing.Literal["Universal", "Recycling", "Argon", "Boron", "Paranid", "Split", "Teladi", "Terran"]


@dataclasses.dataclass(frozen=True, kw_only=True)
class WareFilter:
    include: set[str] | None = None
    exclude: set[str] | None = None

    def __repr__(self):
        return "{}<{} included, {} excluded>".format(
            self.__class__.__qualname__,
            len(self.include) if self.include else "none",
            len(self.exclude) if self.exclude else "none",
        )

    def match(self, ware_id: str) -> bool:
        return self._include(ware_id) and not self._exclude(ware_id)

    def _include(self, ware_id: str) -> bool:
        return ware_id in self.include if self.include else True

    def _exclude(self, ware_id: str) -> bool:
        return ware_id in self.exclude if self.exclude else False


@dataclasses.dataclass(frozen=True)
class Race:
    name: str


@dataclasses.dataclass()
class Faction:
    tag: str
    race: Race
    name: str

    allies: typing.Sequence[str] = ()
    enemies: typing.Sequence[str] = ()
    hostiles: typing.Sequence[str] = ()

    def __str__(self) -> str:
        return f"{self.name} ({self.tag})"

    def exclude(self, exclude: set[str]) -> typing.Self:
        return dataclasses.replace(
            self,
            allies=[x for x in self.allies if x not in exclude],
            enemies=[x for x in self.enemies if x not in exclude],
            hostiles=[x for x in self.hostiles if x not in exclude],
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class Production:
    method: Method
    time: int | None = dataclasses.field(default=None)
    amount: int | None = dataclasses.field(default=None)
    wares: dict[str, int] = dataclasses.field(default_factory=dict)

    colours: typing.ClassVar[typing.Dict[str, str | None]] = {
        "Universal": "rgba(185, 217, 235, 0.90)",
        "Recycling": "rgba(0, 248, 0, 0.25)",
        "Argon": "rgba(55, 55, 255, 0.25)",
        "Boron": "rgba(0, 0, 200, 0.25)",
        "Paranid": "rgba(133, 0, 255, 0.25)",
        "Split": "rgba(255, 0, 0, 0.25)",
        "Teladi": "rgba(245, 245, 39, 0.25)",
        "Terran": "rgba(200, 200, 200, 0.50)",
    }

    def dependencies(self) -> set[str]:
        return set(self.wares.keys())

    def remove_production_input(self, resource_id: str) -> typing.Self:
        wares = {k: v for k, v in self.wares.items() if k != resource_id}
        return dataclasses.replace(self, wares=wares)

    def colour(self) -> str:
        return self.colours[self.method]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Ware:
    key: str
    name: str
    volume: int | None = dataclasses.field(default=None)
    storage: typing.Literal["Container", "Liquid", "Solid", "Condensate"] | None = dataclasses.field(default=None)
    price_min: int | None = dataclasses.field(default=None)
    price_avg: int | None = dataclasses.field(default=None)
    price_max: int | None = dataclasses.field(default=None)
    production: list[Production] = dataclasses.field(default_factory=tuple)

    tags: set[str] = dataclasses.field(default_factory=set)
    colour: str = dataclasses.field(default="lightsteelblue2")

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def id(self) -> str:
        return self.name.lower().replace(" ", "_")

    def dependencies(self) -> set[str]:
        return {d for p in self.production for d in p.dependencies()}

    def fillcolor(self) -> str:
        return self.colour

    def use_production_methods(self, methods: list[Method]) -> typing.Self | None:
        production = {p.method: p for p in self.production}

        for method in methods:
            if selected := production.get(method):
                return dataclasses.replace(self, production=[selected])

        return dataclasses.replace(self, production=[])

    def remove_production_input(self, resource_id: str) -> typing.Self:
        production = [p.remove_production_input(resource_id) for p in self.production]
        return dataclasses.replace(self, production=production)


@dataclasses.dataclass(order=True, frozen=True, kw_only=True)
class Tier:
    level: int
    name: str
    wares: typing.Sequence[Ware]

    def __str__(self) -> str:
        return f"Tier {self.level} ({self.name})"

    def __bool__(self) -> bool:
        return bool(self.wares)

    def dependencies(self) -> set[str]:
        return {d for w in self.wares for d in w.dependencies()}

    def filter_resources(self, wf: WareFilter) -> typing.Self:
        wares = [w for w in self.wares if wf.match(w.key)]
        return dataclasses.replace(self, wares=wares)

    def use_production_methods(self, methods: list[Method]) -> typing.Self:
        wares = [ware.use_production_methods(methods) for ware in self.wares]
        return dataclasses.replace(self, wares=wares)

    def remove_production_input(self, resource_id: str) -> typing.Self:
        wares = [ware.remove_production_input(resource_id) for ware in self.wares]
        return dataclasses.replace(self, wares=wares)


@dataclasses.dataclass(frozen=True)
class Economy:
    tiers: typing.Sequence[Tier] = dataclasses.field(repr=False)

    def __post_init__(self):
        assert isinstance(self.tiers, list)
        for tier in self.tiers:
            assert isinstance(tier, Tier)

    def __repr__(self):
        return "Economy<{} tiers, {} wares>".format(
            len(self.tiers),
            len(self.wares()),
        )

    def tier_ids(self) -> typing.List[int]:
        return [t.level for t in self.tiers]

    def wares(self) -> typing.Mapping[str, Ware]:
        return {resource.key: resource for tier in self.tiers for resource in tier.wares}

    def dependencies(self) -> set[str]:
        wares = {ware.key for tier in self.tiers for ware in tier.wares}
        inputs = {key for tier in self.tiers for key in tier.dependencies()}
        return wares | inputs

    def filter_wares(self, include: set[str] = None) -> typing.Self:
        wf = WareFilter(include=include, exclude=None)
        tiers: list[Tier] = [t.filter_resources(wf) for t in self.tiers]
        new = dataclasses.replace(self, tiers=tiers)
        logger.debug("Filtered wares", wf=wf)
        logger.debug("Old economy", economy=repr(self))
        logger.debug("New economy", economy=repr(new))
        return new

    def filter_tiers(self, tier_ids: set[int]) -> typing.Self:
        tiers: list[Tier] = [t for t in self.tiers if t.level in tier_ids]
        logger.debug("Filtered tiers", tier_ids=tier_ids)
        return dataclasses.replace(self, tiers=tiers)

    def include_tiers(self, tier_ids: set[int]) -> typing.Self:
        logger.debug("Including tiers", economy=self, tier_ids=tier_ids)
        new = self.filter_tiers(tier_ids)
        include = new.dependencies()
        return self.filter_wares(include=include)

    def remove_production_input(self, resource_id: str) -> typing.Self:
        logger.debug("Removing production input", economy=self, resource_id=resource_id)
        tiers: list[Tier] = [t.remove_production_input(resource_id) for t in self.tiers]
        return dataclasses.replace(self, tiers=tiers)

    def filter_production_methods_and_unused_wares(self, methods: list[Method]) -> typing.Self:
        """
        This needs to select wares using only those production methods,
        then find the dependencies of those wares,
        then remove unused production methods from the final list of wares.
        """
        logger.debug("Using production methods", economy=self, methods=methods)

        modified = self.filter_production_methods(methods)
        include = modified.dependencies()
        return modified.filter_wares(include=include)

    def filter_production_methods(self, methods: list[Method]) -> typing.Self:
        """
        Filter production methods.
        This doesn't do any filtering of wares.
        """
        logger.debug("Using production methods", economy=self, methods=methods)
        tiers = [tier.use_production_methods(methods) for tier in self.tiers]
        return dataclasses.replace(self, tiers=tiers)

    def validate(self):
        wares = self.wares()

        if not wares:
            raise Exception(f"No wares in {self!r} economy")

        missing = list()

        for tier in self.tiers:
            for ware in tier.wares:
                for dep in ware.dependencies():
                    if dep not in wares:
                        missing.append((ware, dep))

        if missing:
            description = ", ".join(["{} → {}".format(ware, dep) for ware, dep in missing])
            raise Exception(f"Missing dependencies for {self!r} economy: {description}")
