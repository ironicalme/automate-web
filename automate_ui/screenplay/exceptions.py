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
