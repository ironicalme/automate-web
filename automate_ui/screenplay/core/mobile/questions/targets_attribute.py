from typing import Any

from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.target import Target


class TargetsAttribute:

    def __init__(self, target: Target, target_attribute: str) -> None:
        self.target = target
        self.target_attribute = target_attribute

    def answered_by(self, actor: Actor) -> Any:
        return self.target.found_by(actor).get_attribute(self.target_attribute)

    seen_by = answered_by
