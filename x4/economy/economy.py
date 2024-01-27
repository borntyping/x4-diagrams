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


class Hint(enum.IntFlag):
    NONE = enum.auto()

    SIMPLIFY_INCLUSIVE = enum.auto()
    SIMPLIFY_EXCLUSIVE = enum.auto()


assert Hint.NONE not in Hint.SIMPLIFY_INCLUSIVE | Hint.SIMPLIFY_EXCLUSIVE


@dataclasses.dataclass(frozen=True, kw_only=True)
class Economy:
    wares: typing.Sequence[Ware] = dataclasses.field(repr=False, default=WARES)

    name: str = "X4"
    description: typing.Sequence[str] = ()

    hints: Hint = Hint.NONE

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

    # def __str__(self) -> str:
    #     return self.name

    def __iter__(self) -> typing.Iterator[Ware]:
        return iter(self.wares)

    def __call__(self, name: str) -> typing.Self:
        return self.with_name(name)

    def with_wares(self, wares: typing.Sequence[Ware]) -> typing.Self:
        return dataclasses.replace(self, wares=wares)

    def with_name(self, name: str) -> typing.Self:
        return dataclasses.replace(self, name=name)

    def with_description(self, description: str) -> typing.Self:
        return dataclasses.replace(self, description=(*self.description, description))

    def with_hints(self, hints: Hint) -> typing.Self:
        return dataclasses.replace(self, hints=hints)

    @property
    def tiers(self) -> typing.List[Tier]:
        return list(sorted({ware.tier for ware in self.wares}, key=lambda t: t.key))

    @property
    def recipes(self) -> typing.Sequence[Recipe]:
        return [recipe for ware in self.wares for recipe in ware.recipes]

    def as_dict(self) -> dict[str, Ware]:
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
        inputs = {key for ware in self.wares for key in ware.inputs()}
        return wares | inputs

    def inputs(self) -> set[str]:
        return {key for ware in self.wares for key in ware.inputs()}

    def outputs(self) -> set[str]:
        return {ware.key for ware in self.wares}

    def filter_wares(self, wf: WareFilter) -> typing.Self:
        economy = self.with_wares([ware for ware in self.wares if wf(ware)])
        logger.info("Filtered wares", economy=repr(economy), wf=wf)
        return economy

    def select_tiers(self, tier_ids: set[int]) -> typing.Self:
        """
        Return an economy describing how to make the wares in the given tiers.
        """
        economy: Economy = self.filter_wares(WareInTiers(tier_ids))
        return self._select_inputs_and_outputs(
            inputs=economy.inputs(),
            outputs=economy.outputs(),
        )

    def filter_method(self, priority: typing.Sequence[Method]) -> typing.Self:
        """
        Return an economy describing how to make the wares with the given methods.

        Only one method for each ware will be used, prioritising the first methods in the input sequence.

        This needs to select wares using only those production methods,
        then find the dependencies of those wares,
        then remove unused production methods from the final list of wares.
        """

        # Remove undesired recipes from the economy.
        economy = self.filter_by_method(priority)

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
        economy = economy.remove_all_recipes(only_inputs)

        return economy

    def _focus(self, economy: typing.Self) -> typing.Self:
        """
        Filter wares and recipes to focus on a subset.
        """
        inputs = economy.inputs()
        outputs = economy.outputs()

        # Create an economy containing our inputs *and* outputs.
        economy = self.filter_wares(Include(inputs | outputs))

        # Remove all recipes for wares that are inputs but *not* outputs.
        economy = economy.remove_all_recipes(lambda w: w.key in inputs - outputs)

        # Missile components need hull parts, should that show for T6?

        return economy

    def remove_inputs(self, keys: set[str]) -> typing.Self:
        return self.with_wares([ware.remove_inputs(keys) for ware in self.wares if ware.key not in keys])

    def remove_all_recipes(self, wf: WareFilter) -> typing.Self:
        return self.with_wares([w.with_no_recipes() if wf(w) else w for w in self.wares])

    def filter_by_method(self, priority: typing.Sequence[Method]) -> typing.Self:
        return self.with_wares([ware.with_single_recipe(priority) for ware in self.wares])

    def done(self) -> typing.Self:
        logger.info("Validating economy", economy=repr(self))

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
            raise Exception(f"Missing dependencies for '{self}': {description}")

        return self

    # def filter_recipes(self, f: typing.Callable[[Recipe], bool]) -> typing.Self:
    #     return self.with_wares([ware.filter_recipes(f) for ware in self.wares])

    def remove_common_inputs(self) -> typing.Self | None:
        """Remove wares from both recipe inputs and from the economy."""
        keys = {"energy_cells", "water"}

        wares = self.as_dict()
        names = [wares[c].name.lower() for c in sorted(keys) if c in wares]
        description = "Not shown: {}.".format(p.join(names))

        economy = self.with_name(f"{self.name} simplified").with_description(description).remove_inputs(keys).done()

        for key in keys:
            assert key not in economy.as_dict(), f"{key} still present in {economy}"

        return economy
