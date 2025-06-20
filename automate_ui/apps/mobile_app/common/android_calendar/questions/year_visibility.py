from automate_ui.screenplay.core.actor import Actor
from automate_ui.apps.mobile_app.common.android_calendar.calendar import AndroidCalendar
from automate_ui.screenplay.core.mobile.questions.visible import Visible


class YearVisibility:

    def __init__(self, year: str) -> bool:
        self.year = year

    def answered_by(self, actor: Actor) -> bool:
        return Visible(
            AndroidCalendar.year_picker.year_element(self.year), timeout=2
        ).seen_by(actor)

    seen_by = answered_by
