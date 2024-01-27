import abc
import dataclasses
import enum
import typing

import inflect
import structlog

from x4.types import Method, Recipe, Tier, Ware
from x4_data.economy import WARES

logger = structlog.get_logger(logger_name=__name__)

p = inflect.engine()


class Hint(enum.Flag):
    """
    >>> flags = Hint.SIMPLE_GRAPH | Hint.FULL_SANKEY
    >>> Hint.FULL_GRAPH in flags
    False
    >>> Hint.FULL_SANKEY in flags
    True
    >>> Hint.SIMPLE_GRAPH in flags
    True
    >>> Hint.SIMPLE_SANKEY in flags
    False
    >>> Hint.FULL_GRAPH in Hint.SIMPLE
    False
    >>> Hint.FULL_SANKEY in Hint.SIMPLE
    False
    """

    SIMPLE_GRAPH = enum.auto()
    FULL_GRAPH = enum.auto()

    SIMPLE_SANKEY = enum.auto()
    FULL_SANKEY = enum.auto()

    SIMPLE = SIMPLE_GRAPH | SIMPLE_SANKEY
    FULL_GRAPH_ONLY = FULL_GRAPH | SIMPLE_SANKEY


@dataclasses.dataclass(frozen=True, kw_only=True)
class Economy:
    wares: typing.Sequence[Ware] = dataclasses.field(repr=False, default=WARES)

    name: str = "X4"
    description: typing.Sequence[str] = ()
    hint: Hint = Hint.SIMPLE

    def __post_init__(self):
        assert isinstance(self.wares, typing.Sequence)
        for tier in self.wares:
            assert isinstance(tier, Ware)

    def __repr__(self):
        return "Economy<{self}; {wares} wares, {tiers} tiers, {recipes} recipes>".format(
            self=str(self.name),
            wares=len(self.wares),
            tiers=len(self.tiers),
            recipes=len(self.recipes),
        )

    def __iter__(self) -> typing.Iterator[Ware]:
        return iter(self.wares)

    def __call__(self, name: str, hint: Hint | None = None) -> typing.Self:
        return dataclasses.replace(self, name=name, hint=self.hint if hint is None else hint)

    def with_wares(self, wares: typing.Sequence[Ware]) -> typing.Self:
        economy = dataclasses.replace(self, wares=wares)
        economy.verify()
        return economy

    def with_name(self, name: str) -> typing.Self:
        logger.debug("Replacing name", economy=self, name=name)
        return dataclasses.replace(self, name=name)

    def with_description(self, description: str) -> typing.Self:
        return dataclasses.replace(self, description=(*self.description, description))

    def with_hint(self, hint: Hint) -> typing.Self:
        return dataclasses.replace(self, hint=hint)

    @property
    def tiers(self) -> typing.List[Tier]:
        return list(sorted({ware.tier for ware in self.wares}, key=lambda t: t.key))

    @property
    def recipes(self) -> typing.Sequence[Recipe]:
        return [recipe for ware in self.wares for recipe in ware.recipes]

    def wares_as_dict(self) -> dict[str, Ware]:
        return {ware.key: ware for ware in self.wares}

    def dependencies(self) -> set[str]:
        """
        :deprecated:
        """
        wares = {ware.key for ware in self.wares}
        inputs = {key for ware in self.wares for key in ware.inputs_as_set()}
        return wares | inputs

    def deps(self, wares: typing.Sequence[Ware]) -> set[str]:
        return {key for ware in wares for key in ware.inputs_as_set()}

    def inputs(self) -> set[str]:
        return {key for ware in self.wares for key in ware.inputs_as_set()}

    def outputs(self) -> set[str]:
        return {ware.key for ware in self.wares}

    def outputs_for_ware(self, input_ware: Ware) -> typing.Sequence[Ware]:
        return [ware for ware in self.wares if input_ware.key in ware.inputs_as_set()]

    def select_tiers(self, keys: set[int]) -> typing.Self:
        logger.info("Selecting tiers", economy=self, tiers=keys)

        # Remove all recipes for wares that aren't in the tiers we care about.
        wares = [(ware if ware.tier.key in keys else ware.with_no_recipes()) for ware in self.wares]

        # Remove all wares that aren't in our tier or one we need as an input.
        needs = {key for ware in wares for key in ware.inputs_as_set()}
        wares = [ware for ware in wares if ware.tier.key in keys or ware.key in needs]

        for ware in wares:
            if ware.tier.key in keys and ware.tier.key != 0:
                assert ware.recipes, "Expected ware in the selected tier to have a recipe"

            if ware.tier.key not in keys:
                assert not ware.recipes, "Expected wares not in the selected tier to have all recipes removed"

        return self.with_wares(wares)

    def select_recipe(self, priority: typing.Sequence[Method]) -> typing.Self:
        """Ensure each ware has at most one recipe."""
        logger.info("Selecting a single recipe", economy=self, priority=priority)
        wares = [ware.with_single_recipe(priority) for ware in self.wares]

        for ware in wares:
            for recipe in ware.recipes:
                assert recipe.method in priority, "A recipe was not correctly filtered."

        deps = self.deps(wares)
        wares = [ware for ware in wares if (ware.recipes or ware.key in deps)]

        return self.with_wares(wares)

    def select_recipes(self, *, methods: typing.Set[Method]) -> typing.Self:
        """Remove any recipes that aren't in the given methods."""
        logger.info("Selecting multiple recipes", economy=self, methods=methods)
        wares = [ware.with_selected_recipes(methods) for ware in self.wares]

        for ware in wares:
            for recipe in ware.recipes:
                assert recipe.method in methods, "A recipe was not correctly filtered."

        deps = self.deps(wares)
        wares = [ware for ware in wares if (ware.recipes or ware.key in deps)]

        return self.with_wares(wares)

    def simplify(self) -> typing.Self | None:
        """
        Remove wares that are inputs for a very large number of recipes from the economy,
        which can make graphs much easier to read.

        TODO: replace this with a filter that can be passed to the writers, so graphviz
        TODO: can still show those inputs in the tables.
        """
        keys = {"energy_cells", "water"}
        economy = self.with_wares([ware.remove_inputs(keys) for ware in self.wares if ware.key not in keys])

        # Check we actually removed the inputs.
        for key in keys:
            assert key not in economy.wares_as_dict(), f"{key} still present in {economy}"

        # Add a description recording what was removed.
        wares = self.wares_as_dict()
        names = [wares[c].name.lower() for c in sorted(keys) if c in wares]
        if names:
            description = "Not shown: {}.".format(p.join(names))
            economy = economy.with_description(description)

        return economy

    def verify(self) -> typing.Self:
        logger.info("Validating economy", economy=repr(self))

        if not self.wares:
            raise Exception(f"No wares in {self!r} economy")

        missing = list()

        keys = {ware.key for ware in self.wares}

        for ware in self.wares:
            for recipe in ware.recipes:
                for recipe_input in recipe.inputs:
                    if recipe_input.key not in keys:
                        missing.append((ware, recipe, recipe_input))

        if missing:
            descriptions = [f"{ware} → {recipe.method} → {recipe_input.key}" for ware, recipe, recipe_input in missing]
            raise Exception(f"Missing dependencies for {self}:\n  * {'\n  * '.join(descriptions)}")

        return self
