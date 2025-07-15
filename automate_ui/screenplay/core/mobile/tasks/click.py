from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.target import Target


class Click:
    """
    Clicks on a mobile element

    Args:
        target: The Target of the web element to click on

    Example:
        actor.attempts_to(Click(LoginScreen.login_button))
    """

    def __init__(self, target: Target) -> None:
        self.target = target

    def describe(self) -> str:
        return f"clicks on the {self.target}."

    def perform(self, actor: Actor) -> None:
        self.target.found_by(actor).click()
