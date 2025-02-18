from automate_ui.screenplay.abilities import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor


class CurrentUrl:

    @classmethod
    def answered_by(cls, actor: Actor) -> str:
        page = actor.get_ability(BrowseTheWeb).current_page
        return page.url

    seen_by = answered_by
