from automate_ui.screenplay.actor import Actor
from ..target import Target


class _Texts:

    def __init__(self, target: Target) -> None:
        self.target = target

    def answered_by(self, actor: Actor) -> list[str]:
        return self.target.found_by(actor).all_text_contents()

    seen_by = answered_by


class Text:

    def __init__(self, target: Target) -> None:
        self.target = target

    @classmethod
    def of(cls, target: Target) -> "Text":
        return Text(target)

    @classmethod
    def of_all(cls, target: Target) -> "_Texts":
        return _Texts(target)

    def answered_by(self, actor: Actor) -> str:
        return self.target.found_by(actor).text_content()

    seen_by = answered_by


__all__ = ["Text"]
