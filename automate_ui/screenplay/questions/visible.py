from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class Visible:

    def __init__(self, target: Target) -> None:
        self.target = target

    def answered_by(self, actor: Actor) -> bool:
        return self.target.found_by(actor).is_visible()

    seen_by = answered_by
