from automate_ui.screenplay.core.mobile.target import LocatorStrategy
from automate_ui.screenplay.core.mobile.target import Target

PACKAGE_NAME = "com.example.app"

IOS_DONE_BUTTON = Target.the("'Done' button on iOS keyboard").located_by(
    LocatorStrategy.XPATH, '//XCUIElementTypeButton[@name="Done"]'
)

MAX_SCROLL_ATTEMPTS = 50
