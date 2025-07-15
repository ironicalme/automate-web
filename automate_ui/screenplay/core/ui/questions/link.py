from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class Link:

    def __init__(self, target: Target) -> None:
        self.target = target

    @staticmethod
    def of(target: Target) -> "Link":
        return Link(target)

    def answered_by(self, actor: Actor) -> str:
        return self.target.found_by(actor).get_attribute("href")

    seen_by = answered_by
