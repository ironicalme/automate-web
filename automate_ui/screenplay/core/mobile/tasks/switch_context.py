from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.webdriver import WebDriver
from automate_ui.enums.appium_context import AppiumContext
from automate_ui.screenplay.abilities.use_phone import UsePhone
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.tasks.common import BaseTask
from selenium.common.exceptions import TimeoutException


class SwitchContext(BaseTask):
    def __init__(self, context: AppiumContext, timeout: int = 10) -> None:
        self.context = context
        self.timeout = timeout

    def perform(self, actor: Actor):
        driver = actor.get_ability(UsePhone).driver

        actor.narrate(f"Available contexts: {driver.contexts}")

        def context_available(driver: WebDriver):
            contexts = driver.contexts
            matching_context = next((ctx for ctx in contexts if self.context.value in ctx), None)
            if not matching_context:
                raise RuntimeError(f"No {self.context.value} context was found. Available contexts: {contexts}")
            return matching_context

        try:
            context = WebDriverWait(driver, self.timeout).until(context_available)
        except TimeoutException:
            raise RuntimeError(
                f"Timed out after {self.timeout} seconds while waiting for context '{self.context.value}'."
                f"Available contexts at timeout: {driver.contexts}"
            )

        driver.switch_to.context(context)
        actor.narrate(f"Switched context to: {context}")
