from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.target import Target


class Mark:
    """
    Marks (checks or unchecks) a target element.

    This class represents the action of checking or unchecking a web element,
    typically a checkbox or radio button.  It uses a `Target` to locate the
    element and sets its checked state.

    The `describe` method provides a human-readable description of the action,
    indicating whether the element is being checked or unchecked.  The `perform`
    method executes the action using the provided `Actor` and the `Target`.

    Note:  A log will still be generated even if the web element's state is
    already in the desired status. This indicates that a check/uncheck action
    was attempted.

    Examples:
        actor.attempts_to(Mark.the(my_checkbox, checked=True))  # Check the checkbox
        actor.attempts_to(Mark.the(my_radio_button, checked=False))  # Uncheck the radio button

    Args:
        target: The `Target` representing the element to be marked.
        checked: A boolean indicating whether the element should be checked
            (True) or unchecked (False). Defaults to True.
    """
    def __init__(self, target: Target, checked: bool = True):
        self.target = target
        self.checked = checked

    @staticmethod
    def the(target: Target, checked: bool) -> "Mark":
        return Mark(target=target, checked=checked)

    def describe(self) -> str:
        # Note that in cases where the web element's state is already in desired status a log
        # will still be generated indicating that a checkmark action has taken place.
        if self.checked:
            verb = 'checks'
        else:
            verb = 'unchecks'
        return f'{verb} the {self.target}.'

    def perform(self, actor: Actor):
        self.target.found_by(actor).set_checked(checked=self.checked)
