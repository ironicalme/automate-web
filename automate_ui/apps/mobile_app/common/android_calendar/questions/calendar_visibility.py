from automate_ui.apps.mobile_app.common.android_calendar.calendar import AndroidCalendar
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.questions.visible import Visible


class CalendarVisibility:

    @staticmethod
    def answered_by(actor: Actor) -> bool:
        return Visible(AndroidCalendar.container).seen_by(actor)

    seen_by = answered_by
