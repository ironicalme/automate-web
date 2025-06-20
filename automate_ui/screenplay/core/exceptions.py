from typing import Union


class ScreenPyError(Exception):
    """The base exception for all of ScreenPy."""


class UnableToDirectError(ScreenPyError):
    """The Director cannot direct."""


class UnableToNarrateError(ScreenPyError):
    """The Narrator cannot narrate."""


class UnableToPerformError(ScreenPyError):
    """The Actor lacks the Ability to perform an Action."""


class AbilityError(ScreenPyError):
    """These errors are raised when an Ability fails in some way."""


class ActionError(ScreenPyError):
    """These errors are raised when an Action fails."""


class DeliveryError(ActionError):
    """The Action encountered an error while being performed."""


class UnableToActError(ActionError):
    """The Action is missing key information."""


class NotPerformableError(ScreenPyError):
    """Does not conform to Performable Protocol"""


class TargetingError(ScreenPyError):
    """There was an issue targeting an element."""


class WaitTimeoutError(ScreenPyError):
    """Timeout was exceeded for the Wait task"""


class RestClientNotFoundError(Exception):
    """Exception raised when a requested RestClient is not found."""


class RestClientError(Exception):
    """Exception raised when an HTTP request fails with an unexpected status code."""

    def __init__(
        self, status_code: int, url: str, response_body: Union[dict, str, bytes]
    ):
        self.status_code = status_code
        self.url = url
        self.response_body = response_body
        message = f"HTTP {status_code} Error at {url}: {response_body}"
        super().__init__(message)
