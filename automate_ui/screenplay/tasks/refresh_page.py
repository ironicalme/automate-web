import time

from automate_ui.screenplay.abilities import BrowseTheWeb
from automate_ui.screenplay.actor import Actor


class RefreshPage:
    def __init__(self, wait_time_in_seconds: float = 0.0):
        self._wait_time = wait_time_in_seconds

    @classmethod
    def describe(cls) -> str:
        return 'refreshes the page'

    @classmethod
    def in_seconds(cls, wait_time_in_seconds: float) -> "RefreshPage":
        return RefreshPage(wait_time_in_seconds)

    def perform(self, actor: Actor) -> None:
        time.sleep(self._wait_time)
        page = actor.get_ability(BrowseTheWeb).current_page
        page.reload()
