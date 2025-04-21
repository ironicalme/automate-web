from automate_ui.screenplay.questions.current_url import CurrentUrl
from automate_ui.screenplay.core.actor import Actor


class UrlContains:

    def __init__(self, text: str):
        self.text = text

    def answered_by(self, actor: Actor) -> bool:
        return self.text in CurrentUrl.seen_by(actor)

    seen_by = answered_by
