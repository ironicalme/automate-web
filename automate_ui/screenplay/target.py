from copy import deepcopy
from typing import Optional

from playwright.sync_api import Locator

from .abilities import BrowseTheWeb
from .actor import Actor
from .exceptions import TargetingError
from enum import Enum


class LocatorStrategy(Enum):
    SELECTOR = ("locator", {"selector": None})
    DATA_TEST_ID = ("get_by_test_id", {"test_id": None})
    TEXT = ("get_by_text", {"text": None, "exact": False})
    EXACT_TEXT = ("get_by_text", {"text": None, "exact": True})
    TITLE = ("get_by_title", {"text": None, "exact": False})
    LABEL = ("get_by_label", {"text": None, "exact": False})


class FrameLocatorStrategy(Enum):
    SELECTOR = ("locator", {"selector_or_locator": None})
    DATA_TEST_ID = ("get_by_test_id", {"test_id": None})
    TEXT = ("get_by_text", {"text": None, "exact": False})
    EXACT_TEXT = ("get_by_text", {"text": None, "exact": True})
    TITLE = ("get_by_title", {"text": None, "exact": False})
    LABEL = ("get_by_label", {"text": None, "exact": False})


class Target:
    """
    Represents a target element in a screenplay-based UI automation framework.

    The `Target` class provides a flexible and chainable API to define and locate UI elements
    on a webpage or within an iframe. It supports various locator strategies and allows
    for hierarchical element targeting by specifying parent-child relationships.

    Attributes:
        _description (Optional[str]): A human-readable name for the target.
        locator (Optional[str]): The locator value used to identify the target.
        locator_strategy (Optional[Union[LocatorStrategy, FrameLocatorStrategy]]):
            The strategy used to locate the element.
        page_url (Optional[str]): URL of the page where the target resides (if applicable).
        iframe_locator (Optional[str]): Locator for the iframe containing the target (if applicable).
        index (Optional[int]): The index of the element in case of multiple matches.
        parent (Optional[Target]): The parent `Target` element, if this target is nested.

    Methods:
        the(name: str) -> Target:
            Creates a new `Target` instance with a descriptive name.

        located_by(locator_strategy, locator) -> Target:
            Specifies the locator strategy and value for this target.

        nth(index: int = None) -> Target:
            Specifies the index of the target in case of multiple matches.

        within(parent_target: Target) -> Target:
            Defines a parent `Target` for hierarchical element locating.

        in_iframe_with_locator(iframe_locator: str) -> Target:
            Specifies the iframe locator for the target and creates a new `Target` instance.

        found_by(actor: Actor) -> Locator:
            Resolves the Playwright locator for the target using the specified actor.

    Properties:
        target_name:
            A human-readable name for the target, falling back to the locator if not provided.

    Example:
        Define and locate a target using a chainable API:

        target = Target.the("Submit Button") \
            .located_by(LocatorStrategy.DATA_TEST_ID, "submit-btn") \
            .nth(0) \
            .within(Target.the("Form").located_by(LocatorStrategy.SELECTOR, "#form"))
        submit_button = Target.the("Submit Button in iframe").in_iframe_with_locator("#iframe") \
            .located_by(LocatorStrategy.DATA_TEST_ID, "submit")
    Notes:
        - This class is designed for use in a screenplay-based automation framework.
        - Requires the `Actor` to have the `BrowseTheWeb` ability with an active page.
        - If `locator_strategy` or `locator` is not set before calling `found_by`, a `TargetingError` may occur.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self._description = name
        self.locator = None
        self.locator_strategy = None
        self.page_url = None
        self.iframe_locator = None
        self.index = None
        self.parent: Target = None

    def __repr__(self) -> str:
        return self.target_name

    def __str__(self) -> str:
        return self.target_name

    @staticmethod
    def the(name: str) -> "Target":
        return Target(name)

    def located_by(
        self,
        locator_strategy: LocatorStrategy | FrameLocatorStrategy,
        locator: str
    ):
        self.locator = locator
        self.locator_strategy = locator_strategy
        return self

    def nth(self, index: int = None):
        self.index = index
        return self

    def within(self, parent_target: "Target") -> "Target":
        self.parent = parent_target
        return self

    def in_iframe_with_locator(self, iframe_locator: str) -> "Target":
        self.iframe_locator = iframe_locator
        new_target = deepcopy(self)
        return new_target

    @property
    def target_name(self):
        return self._description if self._description is not None else self.locator

    @target_name.setter
    def target_name(self, value):
        self._description = value

    @target_name.deleter
    def target_name(self):
        del self._description

    def _locator_kwargs(self) -> dict:
        playwright_kwargs = self.locator_strategy.value[1]
        locator_arg = next(iter(playwright_kwargs))
        playwright_kwargs[locator_arg] = self.locator
        return playwright_kwargs

    def found_by(self, actor: Actor) -> Locator:
        """
        All playwright locators are evaluated/resolved here.
        Requires that the actor has the ability to BrowseTheWeb with an active page set.
        """
        page = actor.get_ability(BrowseTheWeb).current_page
        locator_method_name = self.locator_strategy.value[0]

        if page is None:
            raise TargetingError(f"There is no active page! {actor} cannot find the {self}.")
        if not hasattr(page, locator_method_name):
            raise TargetingError(f"Playwright locator method: '{locator_method_name}' not found")

        if self.parent:
            parent_locator_method_name = self.parent.locator_strategy.value[0]
            parent_locator_kwargs = self.parent._locator_kwargs()

            if self.iframe_locator:
                parent_locator: Locator = page.frame_locator(self.iframe_locator) \
                    .__getattribute__(parent_locator_method_name)(**parent_locator_kwargs)
            else:
                parent_locator: Locator = page.__getattribute__(parent_locator_method_name)(**parent_locator_kwargs)

            if self.parent.index is not None:
                parent_locator = parent_locator.nth(self.parent.index)

            locator: Locator = parent_locator.locator(self.locator)

        else:
            if self.iframe_locator:
                locator: Locator = page.frame_locator(self.iframe_locator) \
                    .__getattribute__(locator_method_name)(**self._locator_kwargs())
            else:
                locator: Locator = page.__getattribute__(locator_method_name)(**self._locator_kwargs())

        if self.index is not None:
            return locator.nth(self.index)

        return locator
