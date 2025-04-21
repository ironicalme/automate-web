from typing import Tuple
from certn_qa_tests.screenplay.abilities.use_phone import UsePhone
from certn_qa_tests.screenplay.actor import Actor
from certn_qa_tests.screenplay.mobile.target import Target
from appium.webdriver.webelement import WebElement


@staticmethod
def calculate_element_center(element: WebElement) -> Tuple[int, int]:
    location = element.location
    size = element.size
    return location['x'] + size['width'] // 2, location['y'] + size['height'] // 2


class Tap:
    """
    Taps on the center of a mobile element.
    Currently, supports only single touch point tap.

    Args:
        target: The Target of the web element to tap on

    Example:
        actor.attempts_to(Tap(LoginScreen.login_button))
    """

    def __init__(
        self,
        target: Target
    ) -> None:
        self.target = target

    def describe(self) -> str:
        return f'Taps on the {self.target}.'

    def perform(self, actor: Actor) -> None:
        driver = actor.get_ability(UsePhone).driver
        element = self.target.found_by(actor)
        coord = calculate_element_center(element)
        driver.tap([coord])
