from automate_ui.screenplay.core.actor import Actor
from automate_ui.apps.mobile_app.common.ios_date_picker_wheel.picker_wheel import (
    DatePickerWheel,
)
from automate_ui.screenplay.core.mobile.questions.visible import Visible


class PickerWheelVisibility:

    @staticmethod
    def answered_by(actor: Actor) -> bool:
        return Visible(DatePickerWheel.container, timeout=1).seen_by(actor)

    seen_by = answered_by
