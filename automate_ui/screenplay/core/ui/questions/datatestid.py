from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class _DataTestIDs:

    def __init__(self, target: Target) -> None:
        self.target = target

    def answered_by(self, actor: Actor) -> list[str]:
        return [locator.get_attribute('data-testid') for locator in self.target.found_by(actor).all()]

    seen_by = answered_by


class DataTestID:

    def __init__(self, target: Target) -> None:
        self.target = target

    @staticmethod
    def of(target: Target) -> "DataTestID":
        return DataTestID(target)

    @staticmethod
    def of_all(target: Target) -> "_DataTestIDs":
        return _DataTestIDs(target)

    def answered_by(self, actor: Actor) -> str:
        return self.target.found_by(actor).get_attribute('data-testid')

    seen_by = answered_by
