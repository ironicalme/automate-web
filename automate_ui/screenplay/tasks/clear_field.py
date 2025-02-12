from ..actor import Actor
from ..target import Target


class ClearField:
    """Clears an input field

    Dependency:
        BrowseTheWeb

    Example:
        actor.attempts_to(ClearField(LoginPage.username_field))
    """

    def __init__(self, target: Target) -> None:
        self.target = target

    def describe(self) -> str:
        return f'Clears the "{self.target}".'

    def perform(self, actor: Actor) -> None:
        self.target.found_by(actor).clear()
