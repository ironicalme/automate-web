from automate_ui.enums import Timeouts
from automate_ui.screenplay.abilities import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class Click:
    """
    Clicks on a web element

    Args:
        target: The Target of the web element to click on
        expect_navigation: Expects the click to trigger a page redirect/navigation.

    Raises:
        TimeoutError: Raised if the page navigation does not occur within the specified timeout.

    Dependency:
        BrowseTheWeb

    Example:
        actor.attempts_to(Click(LoginPage.login_button))
    """

    def __init__(self, target: Target, expect_navigation: bool = False) -> None:
        self.target = target
        self.expect_navigation = expect_navigation

    def describe(self) -> str:
        return f"clicks on the {self.target}."

    def perform(self, actor: Actor) -> None:
        if self.expect_navigation:
            page = actor.get_ability(BrowseTheWeb).current_page
            with page.expect_navigation(timeout=Timeouts.PAGE_NAVIGATION * 1000):
                self.target.found_by(actor).click()
        else:
            self.target.found_by(actor).click()
