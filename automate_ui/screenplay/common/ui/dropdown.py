from abc import ABC, abstractmethod
from automate_ui.screenplay.core.ui.target import Target, LocatorStrategy


class Dropdown(ABC):

    def __init__(self, field: Target):
        self._field = field

    @classmethod
    @abstractmethod
    def item(cls, *args: str) -> Target:
        # We could log the text of the item instead of the locator string
        ...

    @property
    def field(self) -> Target:
        return self._field


class DataKeyDropdown(Dropdown):

    @classmethod
    def item(cls, data_key: str) -> Target:
        return Target.the(
            f'dropdown item with data-key: "{data_key}"'
        ).located_by(LocatorStrategy.SELECTOR, f"[data-key='{data_key}']")


class IDDropdown(Dropdown):

    @classmethod
    def item(cls, id_: str) -> Target:
        return Target.the(
            f"dropdown item with id: {id_}"
        ).located_by(LocatorStrategy.SELECTOR, f"[id='{id_}']")


class DataTestIDDropdown(Dropdown):

    @classmethod
    def item(cls, data_test_id_: str) -> Target:
        return Target.the(
            f"dropdown item with matching data-testid: {data_test_id_}"
        ).located_by(LocatorStrategy.DATA_TEST_ID, data_test_id_)


class TextDropdown(Dropdown):

    @classmethod
    def item(cls, text_: str) -> Target:
        return Target.the(
            f"dropdown item with matching text: {text_}"
        ).located_by(LocatorStrategy.TEXT, text_)
