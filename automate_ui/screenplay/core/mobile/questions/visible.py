from selenium.common.exceptions import TimeoutException

from automate_ui.enums.timeouts import Timeouts
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.target import Target


class Visible:
    """
    Checks if an element is visible. The behaviour is similar to Visible for Web UI.

    Visibility check is not instant. Target waits for the element to be available in the DOM,
    before checking for visibility. A custom visibility timeout can be provided.

    Default is defined in Timeouts.MOBILE_VISIBILITY_WAIT

    Returns a boolean

    Usage:
        Visible(BirthDetailsScreen.ios_dob_picker_wheel).seen_by(actor)

        # overriding default timeout
        Visible(BirthDetailsScreen.ios_dob_picker_wheel, timeout=10).seen_by(actor)

    Args:
        target (Target): Target object of the element to check for Visibility
        timeout (float): Optional; override the default timeout set by Timeouts.MOBILE_VISIBILITY_WAIT
    """

    def __init__(
        self, target: Target, timeout: float = Timeouts.MOBILE_VISIBILITY_WAIT
    ) -> None:
        self.target = target
        self.timeout = timeout

    def answered_by(self, actor: Actor) -> bool:
        try:
            # Find the element before checking for is_displayed()
            element = self.target.found_by(actor, timeout=self.timeout)
            return element is not None and element.is_displayed()
        except TimeoutException:
            return False

    seen_by = answered_by
