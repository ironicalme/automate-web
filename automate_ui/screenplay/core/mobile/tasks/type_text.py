import time
from typing import Optional

from automate_ui.screenplay.abilities.use_phone import UsePhone
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.exceptions import UnableToAct
from automate_ui.screenplay.core.mobile.target import Target
from automate_ui.screenplay.core.mobile.tasks.common import BaseTask
from automate_ui.screenplay.core.mobile.tasks.common import register_task
from automate_ui.screenplay.core.mobile.tasks.common import TaskPerformer


def _send_keys_slowly(target: Target, text, actor: Actor, delay=0.05):
    for char in text:
        target.found_by(actor).send_keys(char)
        time.sleep(delay)


class TypeText(TaskPerformer):
    target: Optional[Target]

    def __init__(
        self,
        text: str,
        target: Optional[Target] = None,
        mask: bool = False,
        override: bool = False,
        sequentially: bool = False,
    ) -> None:
        super().__init__(
            TypeText,
            text=text,
            target=target,
            mask=mask,
            override=override,
            sequentially=sequentially,
        )

    @staticmethod
    def secret(text: str) -> "TypeText":
        """
        Provide the text to enter into the field, but mark that the text
        should be masked in the log. The text will appear as "[REDACTED]".
        """
        return TypeText(text=text, mask=True)

    the_password = secret

    def into_the(self, target: Target) -> "TypeText":
        """Target the element to enter text into."""
        self.task_args["target"] = target
        return self

    into = into_the


@register_task(TypeText, "android")
class AndroidTypeText(BaseTask):
    def __init__(
        self,
        target: Target,
        text: str,
        mask: bool,
        override: bool = False,
        sequentially: bool = False,
    ) -> None:
        self.target = target
        self._text = text
        self.mask = mask
        self.override = override
        self.sequentially = sequentially
        self.text_to_log = "[REDACTED]" if mask else text

    def describe(self) -> str:
        if self.text_to_log:
            return f'enters "{self.text_to_log}" into the {self.target}.'
        return f"refrains from typing anything into the {self.target}"

    def perform(self, actor: Actor) -> None:

        if self.target is None:
            raise UnableToAct(
                "Target was not supplied. Provide a Target by using either "
                "the .into() or .into_the() method."
            )

        if not self._text:
            return

        element = self.target.found_by(actor)

        if self.override:
            element.clear()

        if self.sequentially:
            _send_keys_slowly(self.target, self._text, actor)
        else:
            element.send_keys(self._text)


@register_task(TypeText, "ios")
class IosTypeText(BaseTask):
    """
    Taps 1 px above and left of the Target, to hide the keyboard if visible.
    """

    def __init__(
        self,
        target: Target,
        text: str,
        mask: bool,
        override: bool = False,
        sequentially: bool = False,
    ) -> None:
        self.target = target
        self._text = text
        self.mask = mask
        self.override = override
        self.sequentially = sequentially
        self.text_to_log = "[REDACTED]" if mask else text

    def describe(self) -> str:
        if self.text_to_log:
            return f'enters "{self.text_to_log}" into the {self.target}.'
        return f"refrains from typing anything into the {self.target}"

    def perform(self, actor: Actor) -> None:
        driver = actor.get_ability(UsePhone).driver
        if self.target is None:
            raise UnableToAct(
                "Target was not supplied. Provide a Target by using either "
                "the .into() or .into_the() method."
            )

        if not self._text:
            return

        element = self.target.found_by(actor)
        x_coord = element.location["x"]
        y_coord = element.location["y"]
        driver.tap([(x_coord, y_coord)])

        if self.override:
            number_of_backspaces = len(element.text)
            backspaces = "\b" * number_of_backspaces
            element.send_keys(backspaces)

        if self.sequentially:
            _send_keys_slowly(self.target, self._text, actor)
        else:
            element.send_keys(self._text)

        tap_outside_x = element.location["x"] - 1
        tap_outside_y = element.location["y"] - 1
        if driver.is_keyboard_shown():
            driver.tap([(tap_outside_x, tap_outside_y)])
