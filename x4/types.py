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


@dataclasses.dataclass(frozen=True)
class InputWare:
    key: str
    amount: int | None


@dataclasses.dataclass(frozen=True, kw_only=True)
class Recipe:
    method: Method
    time: int | None = dataclasses.field(default=None)
    amount: int | None = dataclasses.field(default=None)
    input_wares: typing.Sequence[InputWare] = dataclasses.field(default_factory=tuple)

    plotly_colours: typing.ClassVar[typing.Dict[str, str | None]] = {
        "Universal": "rgba(185, 217, 235, 0.90)",
        "Recycling": "rgba(0, 248, 0, 0.25)",
        "Argon": "rgba(55, 55, 255, 0.25)",
        "Boron": "rgba(0, 0, 200, 0.25)",
        "Paranid": "rgba(133, 0, 255, 0.25)",
        "Split": "rgba(255, 0, 0, 0.25)",
        "Teladi": "rgba(245, 245, 39, 0.25)",
        "Terran": "rgba(200, 200, 200, 0.50)",
    }

    def plotly_colour(self) -> str:
        return self.plotly_colours[self.method]

    def input_keys(self) -> set[str]:
        return set([i.key for i in self.input_wares])

    def with_input_wares(self, input_wares: typing.Sequence[InputWare]):
        return dataclasses.replace(self, input_wares=input_wares)

    def remove_input(self, *keys: str) -> typing.Self:
        return self.with_input_wares([i for i in self.input_wares if i.key not in keys])


@dataclasses.dataclass(order=True, frozen=True, kw_only=True)
class Tier:
    key: int
    name: str
    # wares: typing.Sequence[Ware]

    def __str__(self) -> str:
        return f"Tier {self.key}: {self.name}"

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
    # def remove_input(self, resource_id: str) -> typing.Self:
    #     wares = [ware.remove_input(resource_id) for ware in self.wares]
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
        return {key for recipe in self.recipes for key in recipe.input_keys()}

    def graphviz_fillcolor(self) -> str:
        return self.colour

    def single_recipe(self, methods: typing.Sequence[Method]) -> typing.Sequence[Recipe]:
        production = {p.method: p for p in self.recipes}
        for method in methods:
            if recipe := production.get(method):
                return [recipe]

        return []

    def with_single_recipe(self, methods: typing.Sequence[Method]) -> typing.Self:
        return self.with_recipes(self.single_recipe(methods))

    def remove_input(self, *keys: str) -> typing.Self:
        return self.with_recipes([p.remove_input(*keys) for p in self.recipes])

    def with_no_recipes(self):
        return self.with_recipes([])

    def with_recipes(self, recipes: typing.Sequence[Recipe]) -> typing.Self:
        return dataclasses.replace(self, recipes=recipes)

    def filter_recipes(self, f: typing.Callable[[Recipe], bool]) -> typing.Self:
        return self.with_recipes([recipe for recipe in self.recipes if f(recipe)])
