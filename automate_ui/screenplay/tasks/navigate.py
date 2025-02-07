from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.actor import Actor


class Navigate:

    def __init__(self, url: str = None) -> None:
        self.url = url

    @staticmethod
    def to_url(url: str) -> "Navigate":
        return Navigate(url)

    def describe(self) -> str:
        return f"navigates to: {self.url}"

    def perform(self, actor: Actor) -> None:
        page = actor.get_ability(BrowseTheWeb).current_page
        page.goto(url=self.url)
