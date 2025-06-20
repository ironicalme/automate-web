from automate_ui.apps.mobile_app.common.components.dropdown import DropdownTray
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.target import Target
from automate_ui.screenplay.core.mobile.tasks.click import Click
from automate_ui.screenplay.core.mobile.tasks.type_text import TypeText


class Select:

    """
    Selects an item from a given dropdown menu.

    Args
        item_text -> str: The item name to select from dropdown items and also
        to type into the dropdown search bar.
        search -> bool: Set as True, to search before selecting.


    Example
        Select("Canada").from_the(BirthDetailsPage.country_dropdown)
            Selects the dropdown item with the "Canada" text.

        Select("Canada", search=True).from_the(BirthDetailsPage.country_dropdown)
            Search the text, then select item with the text, "Canada"

    """

    def __init__(
        self,
        item_text: str = None,
        search: bool = False
    ):
        self.item_text = item_text
        self.search = search
        self.dropdown = None

    def from_the(self, dropdown: Target):
        self.dropdown = dropdown
        return self

    def perform(self, actor: Actor) -> None:
        if not self.dropdown:
            raise Exception("Unable to perform select without target dropdown.")

        actor.attempts_to(Click(self.dropdown))
        if self.search:
            actor.attempts_to(TypeText(self.item_text).into(DropdownTray.search_bar))
        actor.attempts_to(Click(DropdownTray.item(self.item_text)))
