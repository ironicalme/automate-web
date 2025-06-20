from dataclasses import dataclass


@dataclass(frozen=True)
class Timeouts:
    """
    Timeouts for common activities in seconds
    Should prob use a config file or pass in as env vars.
    """
    PAGE_NAVIGATION = 10
    APPIUM_SESSION_TIMEOUT = 300
    APPIUM_WAIT = 30
    MOBILE_VISIBILITY_WAIT = 10