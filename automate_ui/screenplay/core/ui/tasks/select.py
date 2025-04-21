from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.common.ui.dropdown import Dropdown
from typing import Optional


class Select:

    """
    Selects an item from a given dropdown menu.

    Args
        item_name -> str: The text to type into the dropdown field.
        item_locator -> str: The locator string used to find the dropdown item

    Example
        Select("country-united_states", "United States").from_the(Page.country_dropdown)
            Types "United States" and then selects the dropdown item with data-testid='country-united_states'.

    For type hints, refer to the .item() method of the specific Dropdown type used.
    """

    def __init__(
        self,
        item_locator: str = None,
        item_text: Optional[str] = None
    ):
        self.item_text = item_text
        self.item_locator = item_locator
        self.dropdown = None

    def from_the(self, dropdown: Dropdown):
        self.dropdown = dropdown
        return self

    def perform(self, actor: Actor) -> None:
        from automate_ui.screenplay.tasks import Click, TypeText
        if not self.dropdown:
            raise Exception("Unable to perform select without target dropdown.")

        actor.attempts_to(
            Click(self.dropdown.field),
            TypeText(self.item_text).into(self.dropdown.field),
            Click(self.dropdown.item(self.item_locator))
        )
