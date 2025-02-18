from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class Number:

    def __init__(self, target: Target) -> None:
        self.target = target

    @staticmethod
    def of(target: Target) -> "Number":
        return Number(target)

    def answered_by(self, actor: Actor) -> int:
        return self.target.found_by(actor).count()

    seen_by = answered_by
