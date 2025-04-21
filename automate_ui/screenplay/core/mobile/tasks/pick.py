from certn_qa_tests.screenplay.actor import Actor
from certn_qa_tests.screenplay.matchers.is_equal_to import IsEqualTo
from certn_qa_tests.screenplay.mobile.target import Target
from certn_qa_tests.screenplay.mobile.questions.targets_attribute import TargetsAttribute
from certn_qa_tests.screenplay.mobile.tasks.type_text import TypeText
from certn_qa_tests.screenplay.tasks.wait import Wait


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
