from automate_ui.screenplay.actor import Actor
from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
import pathlib
from typing import Literal


class ScreenshotPage:

    def __init__(
        self,
        file_name: str,
        file_type: Literal["png", "jpeg"] = "png"
    ):
        self._file_name = file_name
        self._file_type = file_type

    @classmethod
    def describe(cls) -> str:
        return "takes a screenshot of the current page"

    @classmethod
    def saved_as(
        cls,
        file_name: str,
        file_type: Literal["png", "jpeg"] = "png"
    ) -> "ScreenshotPage":
        return ScreenshotPage(file_name=file_name, file_type=file_type)

    def perform(self, actor: Actor) -> None:
        page = actor.get_ability(BrowseTheWeb).current_page
        path = pathlib.Path(f"{pathlib.Path.cwd()}/screenshots/{self._file_name}")
        page.screenshot(full_page=True, type=self._file_type, path=path)
