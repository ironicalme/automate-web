from pathlib import Path
from typing import List

from automate_ui.screenplay.abilities import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class Upload:
    """
    Upload files or a list of files

    Args:
        target: The target of the add files button
        file_paths: list of file paths. Paths are of type Path

    Dependency:
        BrowseTheWeb

    Example:
        file_paths = [Path("resources/image.png")] OR
        file_paths = [
            Path("resources/image.png"),
            Path("resources/id_card.pdf"),
            Path("resources/log.txt")
        ]
        actor.attempts_to(
            Upload(file_paths).using(Page.upload_files_button)
        )
    """

    def __init__(
        self,
        file_paths: List[Path],
    ) -> None:
        self.target = None
        self.file_paths = file_paths

    def describe(self) -> str:
        return f"Uploads {self.file_paths} using the {self.target.target_name}"

    def using(self, target: Target):
        self.target = target
        return self

    def perform(self, actor: Actor) -> None:
        page = actor.get_ability(BrowseTheWeb).current_page
        if not self.target:
            raise Exception(
                "Unable to upload a file without a target upload button/input"
            )

        with page.expect_file_chooser() as fc_info:
            self.target.found_by(actor).click()
        file_chooser = fc_info.value
        file_chooser.set_files(self.file_paths)

    on_press_of = using
