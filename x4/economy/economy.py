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


class RecipeFilter(typing.Protocol):
    def __call__(self, recipe: "Recipe", inputs: typing.Collection["Ware"], output: "Ware") -> bool:
        ...


@dataclasses.dataclass()
class TierRecipeFilter(RecipeFilter):
    keys: set[int]

    def __call__(self, recipe: "Recipe", inputs: typing.Collection["Ware"], output: "Ware") -> bool:
        return output.tier.key in self.keys


class WareFilter(typing.Protocol):
    def __repr__(self):
        return "{}<{}>".format(self.__class__.__qualname__, self.__partial_repr__())

    @abc.abstractmethod
    def __partial_repr__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, ware: "Ware") -> bool:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True, repr=False)
class WareInTiers(WareFilter):
    keys: set[int]

    def __partial_repr__(self) -> str:
        return "in tier {}".format(", ".join(str(t) for t in self.keys))

    def __call__(self, ware: "Ware") -> bool:
        return ware.tier.key in self.keys


@dataclasses.dataclass(frozen=True, repr=False)
class HasRecipe(WareFilter):
    def __partial_repr__(self) -> str:
        return "has recipe"

    def __call__(self, ware: "Ware") -> bool:
        return bool(ware.recipes)


@dataclasses.dataclass(frozen=True, repr=False)
class Include(WareFilter):
    include: set[str]

    def __partial_repr__(self) -> str:
        return "include {} wares".format(len(self.include))

    def __call__(self, ware: "Ware") -> bool:
        return ware.key in self.include


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

    def with_wares(self, wares: typing.Sequence[Ware], verify: bool = True) -> typing.Self:
        economy = dataclasses.replace(self, wares=wares)

        if verify:
            self.verify()

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

    def filter_by_tier(self, keys: set[int]) -> typing.Self:
        return self._focus(self.filter_wares(lambda w: w.tier.key in keys))

    # def filter_by_recipe(self, f: RecipeFilter) -> typing.Self:
    #     """
    #     :deprecated:
    #     """
    #     logger.info("Filtering by recipe", economy=self, f=f)
    #     wares = self.as_dict()
    #
    #     recipes = [
    #         (recipe, output)
    #         for output in self.wares
    #         for recipe in output.recipes
    #         if f(
    #             recipe=recipe,
    #             inputs=[wares[i.key] for i in recipe.input_wares],
    #             output=output,
    #         )
    #     ]
    #
    #     inputs: set[str] = {key for (recipe, _) in recipes for key in recipe.input_wares}
    #     outputs: set[str] = {output.key for (_, output) in recipes}
    #
    #     economy = self.filter_recipes(lambda recipe: recipe in {r for r, _ in recipes})
    #     logger.info("Filtered recipes", economy=economy, f=f)
    #
    #     economy = economy.filter_wares(Include(inputs | outputs))
    #     logger.info("Filtered wares", economy=economy, f=f)
    #     return economy

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

    def filter_wares(self, wf: WareFilter, verify: bool = True) -> typing.Self:
        return self.with_wares([ware for ware in self.wares if wf(ware)], verify=verify)

    def select_tiers(self, tier_ids: set[int]) -> typing.Self:
        """
        Return an economy describing how to make the wares in the given tiers.
        """
        economy: Economy = self.filter_wares(WareInTiers(tier_ids))
        inputs = economy.inputs()
        outputs = economy.outputs()

        all_wares = Include(inputs | outputs)
        only_inputs = Include(inputs - outputs)

        # Create an economy containing our inputs *and* outputs.
        economy = self.filter_wares(all_wares)

        # Remove all recipes for wares that are inputs but *not* outputs.
        economy = economy.remove_all_recipes(only_inputs)

        return economy

    def _focus(self, economy: typing.Self) -> typing.Self:
        """
        Filter wares and recipes to focus on a subset.
        """
        inputs = economy.inputs()
        outputs = economy.outputs()

        # Create an economy containing our inputs *and* outputs.
        economy = self.filter_wares(Include(inputs | outputs), verify=False)

        # Remove all recipes for wares that are inputs but *not* outputs.
        economy = economy.remove_all_recipes(lambda w: w.key in inputs - outputs, verify=False)

        # Missile components need hull parts, should that show for T6?

        return economy

    def remove_inputs(self, keys: set[str]) -> typing.Self:
        return self.with_wares([ware.remove_inputs(keys) for ware in self.wares if ware.key not in keys])

    def remove_all_recipes(self, wf: WareFilter, *, verify: bool = True) -> typing.Self:
        return self.with_wares([w.with_no_recipes() if wf(w) else w for w in self.wares], verify=verify)

    def with_single_recipe(self, priority: typing.Sequence[Method]) -> typing.Self:
        wares = [ware.with_single_recipe(priority) for ware in self.wares]

        deps = self.deps(wares)
        wares = [ware for ware in wares if ware.recipes or ware.key in deps]

        return self.with_wares(wares)

    def with_selected_recipes(self, methods: typing.Set[Method]) -> typing.Self:
        wares = [ware.with_selected_recipes(methods) for ware in self.wares]

        deps = self.deps(wares)
        wares = [ware for ware in wares if ware.recipes or ware.key in deps]

        return self.with_wares(wares)

    # def filter_recipes(self, f: typing.Callable[[Recipe], bool]) -> typing.Self:
    #     return self.with_wares([ware.filter_recipes(f) for ware in self.wares])

    def verify(self) -> typing.Self:
        logger.info("Validating economy", economy=repr(self))

        if not self.wares:
            raise Exception(f"No wares in {self!r} economy")

        missing = list()

        keys = {ware.key for ware in self.wares}

        for ware in self.wares:
            for dep in ware.inputs_as_set():
                if dep not in keys:
                    missing.append((ware, dep))

        if missing:
            description = ", ".join(["{} → {}".format(ware, dep) for ware, dep in missing])
            raise Exception(f"Missing dependencies for '{self}': {description}")

        return self

    def remove_common_inputs(self) -> typing.Self | None:
        """Remove wares from both recipe inputs and from the economy."""
        keys = {"energy_cells", "water"}
        economy = self.remove_inputs(keys).verify()

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
