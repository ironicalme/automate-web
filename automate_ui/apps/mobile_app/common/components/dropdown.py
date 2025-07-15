from automate_ui.screenplay.core.mobile.target import LocatorStrategy
from automate_ui.screenplay.core.mobile.target import Target


class DropdownTray:

    search_bar = (
        Target.the("Search bar")
        .fallback_locator(
            LocatorStrategy.XPATH,
            '//XCUIElementTypeOther[@name="generic-input" and contains(@label, "Search")]',
            "ios",
        )
        .fallback_locator(
            LocatorStrategy.XPATH,
            '//android.widget.EditText[@text="Search"]',
            "android",
        )
    )

    close_button = (
        Target.the("'Close(X)' button")
        .fallback_locator(LocatorStrategy.ACCESSIBILITY_ID, "close-button", "ios")
        .fallback_locator(
            LocatorStrategy.XPATH,
            '(//android.widget.Button[@resource-id="close-button"])[1]',
            "android",
        )
    )

    @staticmethod
    def item(text: str):
        return (
            Target.the(f"{text}")
            .fallback_locator(
                LocatorStrategy.XPATH,
                f'(//XCUIElementTypeOther[@name="{text}"])[1]',
                "ios",
            )
            .fallback_locator(
                LocatorStrategy.XPATH,
                f'//android.view.ViewGroup[@content-desc="{text}"]',
                "android",
            )
        )
