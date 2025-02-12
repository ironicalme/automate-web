from automate_ui.screenplay.actor import Actor
from ..target import Target


class Value:

    def __init__(self, target: Target) -> None:
        self.target = target

    @staticmethod
    def of(target: Target) -> "Value":
        return Value(target)

    def answered_by(self, actor: Actor) -> str:
        return self.target.found_by(actor).input_value()

    seen_by = answered_by
