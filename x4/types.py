import abc
import dataclasses
import typing

import structlog

logger = structlog.get_logger(logger_name=__name__)


Method = typing.Literal["Universal", "Recycling", "Argon", "Boron", "Paranid", "Split", "Teladi", "Terran"]


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
class Recipe:
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

    def inputs(self) -> set[str]:
        return set(self.wares.keys())

    def remove_production_input(self, resource_id: str) -> typing.Self:
        wares = {k: v for k, v in self.wares.items() if k != resource_id}
        return dataclasses.replace(self, wares=wares)

    def colour(self) -> str:
        return self.colours[self.method]


@dataclasses.dataclass(order=True, frozen=True, kw_only=True)
class Tier:
    key: int
    name: str
    # wares: typing.Sequence[Ware]

    def __str__(self) -> str:
        return f"Tier {self.key} ({self.name})"

    # def __bool__(self) -> bool:
    #     return bool(self.wares)
    #
    # def dependencies(self) -> set[str]:
    #     return {d for w in self.wares for d in w.dependencies()}
    #

    #
    # def use_recipes(self, methods: typing.Sequence[Method]) -> typing.Self:
    #     wares = [ware.with_single_recipe(methods) for ware in self.wares]
    #     return dataclasses.replace(self, wares=wares)
    #
    # def remove_production_input(self, resource_id: str) -> typing.Self:
    #     wares = [ware.remove_production_input(resource_id) for ware in self.wares]
    #     return dataclasses.replace(self, wares=wares)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Ware:
    key: str
    name: str
    tier: Tier
    volume: int | None = dataclasses.field(default=None)
    storage: typing.Literal["Container", "Liquid", "Solid", "Condensate"] | None = dataclasses.field(default=None)
    price_min: int | None = dataclasses.field(default=None)
    price_avg: int | None = dataclasses.field(default=None)
    price_max: int | None = dataclasses.field(default=None)
    recipes: typing.Sequence[Recipe] = dataclasses.field(default_factory=tuple)

    tags: set[str] = dataclasses.field(default_factory=set)
    colour: str = dataclasses.field(default="lightsteelblue2")

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def id(self) -> str:
        return self.name.lower().replace(" ", "_")

    def inputs(self) -> set[str]:
        return {key for recipe in self.recipes for key in recipe.inputs()}

    def graphviz_fillcolor(self) -> str:
        return self.colour

    def single_recipe(self, methods: typing.Sequence[Method]) -> typing.Sequence[Recipe]:
        production = {p.method: p for p in self.recipes}
        for method in methods:
            if recipe := production.get(method):
                return [recipe]

        return []

    def use_method(self, methods: typing.Sequence[Method]) -> typing.Self:
        return dataclasses.replace(self, recipes=self.single_recipe(methods))

    def remove_production_input(self, resource_id: str) -> typing.Self:
        recipes = [p.remove_production_input(resource_id) for p in self.recipes]
        return dataclasses.replace(self, recipes=recipes)

    def with_no_recipes(self):
        return dataclasses.replace(self, recipes=[])


class WareFilter:
    def __repr__(self):
        return "{}<{}>".format(self.__class__.__qualname__, self.__partial_repr__())

    @abc.abstractmethod
    def __partial_repr__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def match(self, ware: "Ware") -> bool:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class InTiers(WareFilter):
    tier_keys: set[int]

    def __partial_repr__(self) -> str:
        return "in tier {}".format(", ".join(self.tier_keys))

    def match(self, ware: "Ware") -> bool:
        return ware.tier.key in self.tier_keys


@dataclasses.dataclass(frozen=True)
class HasRecipe(WareFilter):
    def __partial_repr__(self) -> str:
        return "has recipe"

    def match(self, ware: "Ware") -> bool:
        return bool(ware.recipes)


@dataclasses.dataclass(frozen=True)
class Include(WareFilter):
    include: set[str]

    def __partial_repr__(self) -> str:
        return "include {} wares".format(len(self.include))

    def match(self, ware: "Ware") -> bool:
        return ware.key in self.include


@dataclasses.dataclass(frozen=True)
class Economy:
    wares: typing.Sequence[Ware] = dataclasses.field(repr=False)

    def __post_init__(self):
        assert isinstance(self.wares, list)
        for tier in self.wares:
            assert isinstance(tier, Ware)

    def __repr__(self):
        return "Economy<{self}, {wares} wares, {tiers} tiers, {recipes} recipes>".format(
            self=self,
            wares=len(self.wares),
            tiers=len(self.tiers),
            recipes=len(self.recipes),
        )

    def __iter__(self) -> typing.Iterator[Ware]:
        return iter(self.wares)

    @property
    def tiers(self) -> typing.List[Tier]:
        return list(sorted({ware.tier for ware in self.wares}, key=lambda t: t.key))

    @property
    def recipes(self) -> typing.Sequence[Recipe]:
        return [recipe for ware in self.wares for recipe in ware.recipes]

    def as_dict(self) -> dict[str, Ware]:
        return {ware.key: ware for ware in self.wares}

    def dependencies(self) -> set[str]:
        """
        :deprecated:
        """
        wares = {ware.key for ware in self.wares}
        inputs = {key for ware in self.wares for key in ware.inputs()}
        return wares | inputs

    def inputs(self) -> set[str]:
        return {key for ware in self.wares for key in ware.inputs()}

    def outputs(self) -> set[str]:
        return {ware.key for ware in self.wares}

    def with_wares(self, wares: typing.Sequence[Ware]) -> typing.Self:
        return dataclasses.replace(self, wares=wares)

    def filter_wares(self, wf: WareFilter) -> typing.Self:
        return self.with_wares([ware for ware in self.wares if wf.match(ware)])

    def select_tiers(self, tier_ids: set[int]) -> typing.Self:
        """
        Return an economy describing how to make the wares in the given tiers.
        """
        economy: Economy = self.filter_wares(InTiers(tier_ids))
        return self._select_inputs_and_outputs(
            inputs=economy.inputs(),
            outputs=economy.outputs(),
        )

    def select_method(self, priority: typing.Sequence[Method]) -> typing.Self:
        """
        Return an economy describing how to make the wares with the given methods.

        Only one method for each ware will be used, prioritising the first methods in the input sequence.

        This needs to select wares using only those production methods,
        then find the dependencies of those wares,
        then remove unused production methods from the final list of wares.
        """

        # Remove undesired recipes from the economy.
        economy = self.remove_unwanted_recipes(priority)

        # Select wares that still have a recipe.
        wares_with_recipe = economy.filter_wares(HasRecipe())

        return self._select_inputs_and_outputs(
            inputs=wares_with_recipe.inputs(),
            outputs=wares_with_recipe.outputs(),
        )

    def _select_inputs_and_outputs(self, inputs: set[str], outputs: set[str]):
        all_wares = Include(inputs | outputs)
        only_inputs = Include(inputs - outputs)

        # Create an economy containing our inputs *and* outputs.
        economy = self.filter_wares(all_wares)

        # Remove all recipes for wares that are inputs but *not* outputs.
        economy = self.remove_all_recipes(only_inputs)

        return economy

    def remove_production_input(self, key: str) -> typing.Self:
        return self.with_wares([ware.remove_production_input(key) for ware in self.wares])

    def remove_all_recipes(self, wf: WareFilter) -> typing.Self:
        return self.with_wares([w.with_no_recipes() if wf.match(w) else w for w in self.wares])

    def remove_unwanted_recipes(self, priority: typing.Sequence[Method]) -> typing.Self:
        return self.with_wares([ware.use_method(priority) for ware in self.wares])

    def validate(self) -> typing.Self:
        logger.info("Validating economy", economy=self)

        if not self.wares:
            raise Exception(f"No wares in {self!r} economy")

        missing = list()

        keys = {ware.key for ware in self.wares}

        for ware in self.wares:
            for dep in ware.inputs():
                if dep not in keys:
                    missing.append((ware, dep))

        if missing:
            description = ", ".join(["{} → {}".format(ware, dep) for ware, dep in missing])
            raise Exception(f"Missing dependencies for {self!r} economy: {description}")

        return self
