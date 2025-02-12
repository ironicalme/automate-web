from automate_ui.screenplay.actor import Actor
from ..target import Target


class _AriaLabels:
    """
    Returns the aria-labels of the Target
    """

    def __init__(self, target: Target) -> None:
        self.target = target

    def seen_by(self, actor: Actor) -> list[str]:
        return [locator.get_attribute('aria-label') for locator in self.target.found_by(actor).all()]


class AriaLabel:
    """
    Returns the aria-label of the Target
    """

    def __init__(self, target: Target) -> None:
        self.target = target

    @staticmethod
    def of(target: Target) -> "AriaLabel":
        return AriaLabel(target)

    @staticmethod
    def of_all(target: Target) -> "_AriaLabels":
        return _AriaLabels(target)

    def seen_by(self, actor: Actor) -> str:
        return self.target.found_by(actor).get_attribute('aria-label')


__all__ = ["AriaLabel"]
