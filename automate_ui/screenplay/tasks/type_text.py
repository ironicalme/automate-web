from typing import Optional

from ..actor import Actor
from ..exceptions import UnableToActError
from ..target import Target


class TypeText:

    target: Optional[Target]

    def __init__(
        self,
        text: str,
        mask: bool = False,
        sequentially: bool = False,
        override: bool = True
    ) -> None:
        self._text = text
        self.target = None
        self.sequentially = sequentially
        self.override = override

        if mask:
            self.text_to_log = "[REDACTED]"
        else:
            self.text_to_log = text

    @staticmethod
    def secret(text: str) -> "TypeText":
        """
        Provide the text to enter into the field, but mark that the text
        should be masked in the log. The text will appear as "[CENSORED]".
        """
        return TypeText(text, mask=True)

    the_password = secret

    def into_the(self, target: Target, sequentially: bool = False) -> "TypeText":
        """Target the element to enter text into."""
        self.target = target
        self.sequentially = sequentially
        return self

    into = into_the

    def describe(self) -> str:
        if self.text_to_log:
            return f'enters "{self.text_to_log}" into the {self.target}.'
        return f'refrains from typing anything into the {self.target}'

    def perform(self, actor: Actor) -> None:
        if self.target is None:
            raise UnableToActError(
                "Target was not supplied for Enter. Provide a Target by using either "
                "the .into() or .into_the() method."
            )

        # Playwright will throw a TypeError if no text is passed into the .fill() method.
        # The data models in this framework support None fields.
        # The desired behaviour of entering None is to leave any pre-filled data as is and skip the action.
        if not self._text:
            return

        target = self.target.found_by(actor)

        if self.override:
            target.clear()

        if self.sequentially:
            target.press_sequentially(self._text)
        else:
            target.fill(self._text)
