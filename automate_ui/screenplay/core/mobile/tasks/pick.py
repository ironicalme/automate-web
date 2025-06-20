from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.matchers.is_equal_to import IsEqualTo
from automate_ui.screenplay.core.mobile.target import Target
from automate_ui.screenplay.core.mobile.questions.targets_attribute import TargetsAttribute
from automate_ui.screenplay.core.mobile.tasks.type_text import TypeText
from automate_ui.screenplay.core.ui.tasks.wait import Wait


class Pick:
    """
    Sets the value on the picker wheel with retry logic.

    Args:
        value (str): The value to set on the picker.

    """

    def __init__(self, value: str) -> None:
        self.value = value

    def from_wheel(self, target: Target) -> "Pick":
        """Target the wheel element to pick from."""
        self.target = target
        return self

    def perform(self, actor: Actor):

        actor.attempts_to(
            TypeText(self.value).into_the(self.target),
            Wait()
            .until(TargetsAttribute(self.target, "value"), IsEqualTo(self.value))
            .after_failed_attempt(TypeText(self.value).into_the(self.target))
        )
