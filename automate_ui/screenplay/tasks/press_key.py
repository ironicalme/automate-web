from automate_ui.enums.keyboard_key import KeyboardKey
from automate_ui.screenplay.abilities import BrowseTheWeb
from automate_ui.screenplay.actor import Actor


class PressKey:

    def __init__(self, key: KeyboardKey) -> None:
        self.key = str(key.value)

    def describe(self) -> str:
        return f'presses the "{self.key}" key'

    def perform(self, actor: Actor) -> None:
        keyboard = actor.get_ability(BrowseTheWeb).current_page.keyboard
        keyboard.press(key=self.key)
