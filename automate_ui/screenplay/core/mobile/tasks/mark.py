from certn_qa_tests.screenplay.abilities.use_phone import UsePhone
from certn_qa_tests.screenplay.actor import Actor
from certn_qa_tests.screenplay.exceptions import WaitTimeoutError
from certn_qa_tests.screenplay.matchers import IsNotEqualTo
from certn_qa_tests.screenplay.mobile.target import Target
from certn_qa_tests.screenplay.mobile.tasks.common import (
    BaseTask,
    register_task,
    TaskPerformer
)
from certn_qa_tests.screenplay.tasks import Wait
from certn_qa_tests.screenplay.mobile.questions import TargetsAttribute


class Mark(TaskPerformer):
    def __init__(self, target: Target, checked: bool = True) -> None:
        super().__init__(Mark, target=target, checked=checked)

    @staticmethod
    def the(target: Target, checked: bool) -> "Mark":
        return Mark(target, checked)


@register_task(Mark, "android")
class AndroidMark(BaseTask):

    def __init__(self, target: Target, checked: bool = True) -> None:
        self.target = target
        self.checked = checked

    def describe(self) -> str:
        action = "checks" if self.checked else "unchecks"
        return f"{action} the {self.target}."

    def perform(self, actor: Actor):
        is_checked__before_action = self.target.found_by(actor).get_attribute("checked")
        if is_checked__before_action != self.checked:
            self.target.found_by(actor).click()

        try:
            Wait().until(TargetsAttribute(self.target, "value"), IsNotEqualTo(is_checked__before_action))
        except Exception:
            raise WaitTimeoutError(
                f"{actor.name} was unsuccessful in checking/unchecking the checkbox {self.target.target_name}. "
                f"Expected state: {'checked' if self.checked else 'unchecked'}."
            )


@register_task(Mark, "ios")
class IosMark(BaseTask):

    def __init__(self, target: Target, checked: bool = True) -> None:
        self.target = target
        self.checked = checked

    def describe(self) -> str:
        action = "checks" if self.checked else "unchecks"
        return f"{action} the {self.target}."

    def perform(self, actor: Actor):
        is_checked__before_action = self.target.found_by(actor).get_attribute("value")
        driver = actor.get_ability(UsePhone).driver
        if (is_checked__before_action == 'unchecked' and self.checked) or (is_checked__before_action == 'checked' and not self.checked):
            element = self.target.found_by(actor)
            x_coord = element.location["x"]
            y_coord = element.location["y"]
            offset_x = offset_y = 20  # offset a little bit to ensure it taps inside the element. Cannot tap center since some elements have a link like `Privacy policy` in the center.
            driver.tap([(x_coord + offset_x, y_coord + offset_y)])

        try:
            Wait().until(TargetsAttribute(self.target, "value"), IsNotEqualTo(is_checked__before_action))
        except Exception:
            raise WaitTimeoutError(
                f"{actor.name} was unsuccessful in checking/unchecking the checkbox {self.target.target_name}. "
                f"Expected state: {'checked' if self.checked else 'unchecked'}."
            )
