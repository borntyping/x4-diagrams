import dataclasses
import typing


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
class Resource:
    name: str
    race: str | None = dataclasses.field(default=None)
    tags: set[str] = dataclasses.field(default_factory=set)
    colour: str = dataclasses.field(default="lightsteelblue2")
    recipes: dict[str, set[str]] = dataclasses.field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def id(self) -> str:
        return self.name.lower().replace(" ", "")

    def fillcolor(self) -> str:
        if self.race == "Argon":
            return "green"
        elif self.race == "Paranid":
            return "blue"
        if self.race == "Teladi":
            return "yellow"

        return self.colour

    def inputs(self):
        if not self.recipes:
            return ()

        always = set.intersection(*self.recipes.values())
        for input_resource_name in always:
            yield "always", input_resource_name

        for recipe, input_resource_names in self.recipes.items():
            for input_resource_name in input_resource_names - always:
                yield recipe, input_resource_name

    def inputs_for_variant(self, variant: str) -> set[str]:
        return self.recipes.get(variant, self.recipes.get("Universal", set()))

    def all_inputs(self) -> set[str]:
        return {i for inputs in self.recipes.values() for i in inputs}

    def filter_recipes(self, resources: set[str]) -> typing.Self:
        return dataclasses.replace(
            self,
            recipes={variant: {r for r in inputs if r in resources} for variant, inputs in self.recipes.items()},
        )


@dataclasses.dataclass(order=True, frozen=True)
class Tier:
    level: int
    name: str
    resources: typing.Sequence[Resource]

    def __str__(self) -> str:
        return f"Tier {self.level} ({self.name})"

    def __bool__(self) -> bool:
        return bool(self.resources)

    def filter_resources(self, names: set[str]) -> typing.Self:
        resources = [r.filter_recipes(names) for r in self.resources if r.name in names]
        return dataclasses.replace(self, resources=resources)
