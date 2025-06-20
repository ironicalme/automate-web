from automate_ui.screenplay.core.actor import Actor
from automate_ui.apps.mobile_app.common.ios_date_picker_wheel.picker_wheel import (
    DatePickerWheel,
)
from automate_ui.screenplay.core.mobile.questions.targets_attribute import (
    TargetsAttribute,
)


class SelectedMonth:

    @staticmethod
    def answered_by(actor: Actor) -> str:
        return TargetsAttribute(DatePickerWheel.selected_month, "value").seen_by(actor)

    seen_by = answered_by
