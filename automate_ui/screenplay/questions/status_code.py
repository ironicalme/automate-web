from automate_ui.screenplay.actor import Actor
from automate_ui.screenplay.questions.response import Response


class StatusCode:

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def of_request(cls, name: str) -> "StatusCode":
        return StatusCode(name)

    def sent_by(self, actor: Actor) -> int:
        return Response(self.name).sent_by(actor).status_code


