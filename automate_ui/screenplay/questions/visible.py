from automate_ui.screenplay.actor import Actor
from automate_ui.screenplay.target import Target, LocatorStrategy


class Visible:

    def __init__(self, target: Target) -> None:
        self.target = target

    def answered_by(self, actor: Actor) -> bool:
        return self.target.found_by(actor).is_visible()

    seen_by = answered_by
