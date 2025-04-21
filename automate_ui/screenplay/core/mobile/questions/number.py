from certn_qa_tests.screenplay.actor import Actor
from ..target import Target


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
