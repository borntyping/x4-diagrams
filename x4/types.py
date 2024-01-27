import dataclasses
import functools
import typing

import structlog

from x4.colours import Palette

logger = structlog.get_logger(logger_name=__name__)


type Method = typing.Literal[
    "Universal", "Recycling+Universal", "Argon", "Boron", "Paranid", "Split", "Teladi", "Terran", "Recycling+Terran"
]
type Storage = typing.Literal["Container", "Liquid", "Solid", "Condensate"]


@dataclasses.dataclass(frozen=True)
class Race:
    name: str
    colour: Palette


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


@dataclasses.dataclass(order=True, frozen=True, kw_only=True)
class Tier:
    key: int
    name: str
    colour: Palette

    def __str__(self) -> str:
        return f"T{self.key}: {self.name}"


@dataclasses.dataclass(frozen=True)
class RecipeInput:
    key: str
    amount: int | None


@dataclasses.dataclass(frozen=True, kw_only=True)
class Recipe:
    method: Method
    time: int | None = dataclasses.field(default=None)
    amount: int | None = dataclasses.field(default=None)
    inputs: typing.Sequence[RecipeInput] = dataclasses.field(default_factory=tuple)

    def inputs_as_set(self) -> set[str]:
        return set([i.key for i in self.inputs])


@dataclasses.dataclass(frozen=True, kw_only=True)
class Ware:
    key: str
    name: str
    acronym: str
    tier: Tier
    colour: Palette = dataclasses.field(repr=False)

    volume: int | None = dataclasses.field(default=None, repr=False)
    storage: typing.Literal["Container", "Liquid", "Solid", "Condensate"] | None = dataclasses.field(default=None, repr=False)
    price_min: int | None = dataclasses.field(default=None, repr=False)
    price_avg: int | None = dataclasses.field(default=None, repr=False)
    price_max: int | None = dataclasses.field(default=None, repr=False)
    recipes: typing.Sequence[Recipe] = dataclasses.field(default_factory=tuple, repr=False)

    tags: set[str] = dataclasses.field(default_factory=set, repr=False)

    def __str__(self) -> str:
        return f"{self.name}"

    @functools.cached_property
    def id(self) -> str:
        return self.name.lower().replace(" ", "_")

    @functools.cached_property
    def acronym(self) -> str:
        return "".join(part[0] for part in self.name.split())

    def inputs_as_set(self) -> set[str]:
        return {key for recipe in self.recipes for key in recipe.inputs_as_set()}

    @functools.cached_property
    def graphviz_fillcolor(self) -> str:
        return self.colour

    @functools.cached_property
    def gv_bg_colour(self) -> str:
        return "white"

    @functools.cached_property
    def gv_fg_colour(self) -> str:
        return self.colour

    def single_recipe(self, methods: typing.Sequence[Method]) -> typing.Sequence[Recipe]:
        production = {p.method: p for p in self.recipes}
        for method in methods:
            if recipe := production.get(method):
                return [recipe]

        return []

    def with_single_recipe(self, methods: typing.Sequence[Method]) -> typing.Self:
        return self.with_recipes(self.single_recipe(methods))

    def with_selected_recipes(self, methods: typing.Set[Method]) -> typing.Self:
        return self.with_recipes([r for r in self.recipes if r.method in methods])

    def with_no_recipes(self):
        return self.with_recipes([])

    def with_recipes(self, recipes: typing.Sequence[Recipe]) -> typing.Self:
        return dataclasses.replace(self, recipes=recipes)

    def filter_recipes(self, f: typing.Callable[[Recipe], bool]) -> typing.Self:
        return self.with_recipes([recipe for recipe in self.recipes if f(recipe)])
