from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.target import Target


class Number:

    def __init__(self, target: Target) -> None:
        self.target = target

    @staticmethod
    def of(target: Target) -> "Number":
        return Number(target)

    def answered_by(self, actor: Actor) -> int:
        element_list = self.target.find_all_by(actor)
        return len(element_list)

    seen_by = answered_by
