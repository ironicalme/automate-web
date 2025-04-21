from certn_qa_tests.screenplay.actor import Actor
from ..target import Target


class Text:

    def __init__(self, target: Target) -> None:
        self.target = target

    @classmethod
    def of(cls, target: Target) -> "Text":
        return Text(target)

    def answered_by(self, actor: Actor) -> str:
        return self.target.found_by(actor).text

    seen_by = answered_by
