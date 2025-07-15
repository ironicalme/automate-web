from enum import Enum
from typing import Literal, Optional, Union

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from automate_ui.enums import Timeouts
from automate_ui.screenplay.abilities.use_phone import UsePhone
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.exceptions import TargetingError


class LocatorStrategy(Enum):
    ACCESSIBILITY_ID = {"by": "AppiumBy.ACCESSIBILITY_ID", "value": None}
    ID = {"by": "AppiumBy.ID", "value": None}
    CLASS_NAME = {"by": "AppiumBy.CLASS_NAME", "value": None}
    XPATH = {"by": "AppiumBy.XPATH", "value": None}
    NAME = {"by": "AppiumBy.NAME", "value": None}

    # CSS_SELECTOR should only be used for elements in Web View
    CSS_SELECTOR = {"by": "AppiumBy.CSS_SELECTOR", "value": None}


class Target:
    """Wrapper for appium locators.

    Primary locators are fed using located_by. They are optional.

    Fallback locators are fed using fallback_locator.

    General guidelines:

    If element appears on multiple platform and Accessibility ID is available ->
    use primary locator strategy as Accessibility ID:

        email_field = Target.the("Email field").located_by(LocatorStrategy.ACCESSIBILITY_ID, "email")

    If Accessibility ID is not available, use only fallback locators:

        email_field = Target.the("'Email' field")

        .fallback_locator(LocatorStrategy.XPATH, "//android.widget.EditText[@resource-id='email']", "android")

        .fallback_locator(LocatorStrategy.XPATH, "//XCUIElementTypeTextField[@name='email']", "ios")

    If POM appears only for one or the other platform -> use primary locator with
    any suitable Strategy:

        android_agree_to_terms = Target.the("Agree to terms")

        .located_by(LocatorStrategy.ID, "com.android.chrome:id/terms_accept")

    """

    def __init__(self, name: Optional[str] = None) -> None:
        self._description = name
        self.locator = None
        self.locator_strategy = None
        self.fallback_locators = []

    def __repr__(self) -> str:
        return self.target_name

    def __str__(self) -> str:
        return self.target_name

    @property
    def target_name(self):
        return self._description if self._description is not None else self.locator

    @target_name.setter
    def target_name(self, value):
        self._description = value

    @target_name.deleter
    def target_name(self):
        del self._description

    @staticmethod
    def the(name: str) -> "Target":
        return Target(name)

    def located_by(
        self,
        primary_locator: Optional[LocatorStrategy] = None,
        locator: Optional[str] = None,
    ) -> "Target":
        """Set an optional, primary locator"""
        self.locator = locator
        self.locator_strategy = primary_locator
        return self

    def fallback_locator(
        self,
        locator_strategy: LocatorStrategy,
        locator: str,
        platform: Union[Literal["android"], Literal["ios"]],
    ) -> "Target":
        """Add a platform-specific fallback locator."""
        self.fallback_locators.append((locator_strategy, locator, platform))
        return self

    def _locator_kwargs(self) -> dict:
        appium_kwargs = self.locator_strategy.value
        iterator = iter(appium_kwargs)
        next(iterator)
        locator_arg = next(iterator)
        appium_kwargs[locator_arg] = self.locator
        return appium_kwargs

    def _wait_for(
        self, driver, locator_kwargs, timeout: float, multiple: bool
    ) -> Union[WebElement, list[WebElement]]:
        """Generic wait function to handle both single and multiple elements."""
        wait = WebDriverWait(
            driver,
            timeout=timeout,
            poll_frequency=1,
            ignored_exceptions=[ElementNotSelectableException, NoSuchElementException],
        )
        by = getattr(AppiumBy, self.locator_strategy.name)
        return wait.until(
            lambda x: (
                x.find_elements(by=by, value=locator_kwargs["value"])
                if multiple
                else x.find_element(by=by, value=locator_kwargs["value"])
            )
        )

    def _find_element_with_fallback(
        self, actor: Actor, timeout: float, multiple: bool
    ) -> Union[WebElement, list[WebElement]]:
        """
        Tries to find an element using the primary locator, falling back if necessary.
        Returns a single WebElement if multiple=False, or a list of elements if multiple=True.
        """
        driver = actor.get_ability(UsePhone).driver
        platform = driver.capabilities.get("platformName").lower()

        if driver is None:
            raise TargetingError(
                f"There is no active mobile session! {actor} cannot find the {self}."
            )

        if not self.locator_strategy:
            self._set_locator_from_fallback(platform)

        if not self.locator_strategy:
            raise TargetingError(
                f"There is no primary or fallback locator defined for {self.target_name} on {platform}"
            )

        locator_strategy_name = self.locator_strategy.name
        if not hasattr(AppiumBy, locator_strategy_name):
            raise TargetingError(
                f"AppiumBy locator method: '{locator_strategy_name}' not found/implemented"
            )

        try:
            return self._wait_for(driver, self._locator_kwargs(), timeout, multiple)
        except TimeoutException:
            return self._try_fallback_locators(driver, platform, timeout, multiple)

    def found_by(
        self, actor: Actor, timeout: float = Timeouts.APPIUM_WAIT
    ) -> WebElement:
        """Finds a single element using the primary locator or fallback."""
        return self._find_element_with_fallback(actor, timeout, multiple=False)

    def find_all_by(
        self, actor: Actor, timeout: float = Timeouts.APPIUM_WAIT
    ) -> list[WebElement]:
        """Finds all matching elements using the primary locator or fallback."""
        return self._find_element_with_fallback(actor, timeout, multiple=True)

    def _set_locator_from_fallback(self, platform: str):
        for (
            fallback_strategy,
            fallback_locator,
            fallback_platform,
        ) in self.fallback_locators:
            if fallback_platform == platform:
                self.locator_strategy = fallback_strategy
                self.locator = fallback_locator
                break

    def _try_fallback_locators(
        self, driver, platform: str, timeout: float, multiple: bool
    ) -> Union[WebElement, list[WebElement]]:
        """Tries fallback locators if the primary one fails."""
        for (
            fallback_strategy,
            fallback_locator,
            fallback_platform,
        ) in self.fallback_locators:
            if fallback_platform == platform:
                self.locator_strategy = fallback_strategy
                self.locator = fallback_locator
                locator_kwargs = self._locator_kwargs()
                try:
                    return self._wait_for(driver, locator_kwargs, timeout, multiple)
                except TimeoutException:
                    continue
        return [] if multiple else None
