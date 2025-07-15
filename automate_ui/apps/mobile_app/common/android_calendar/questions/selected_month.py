from datetime import datetime

from automate_ui.apps.mobile_app.common.android_calendar.calendar import AndroidCalendar
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.questions.targets_attribute import (
    TargetsAttribute,
)


class SelectedMonth:
    """
    Returns the month number as string
    """

    @staticmethod
    def answered_by(actor: Actor) -> str:
        text = TargetsAttribute(
            AndroidCalendar.month_and_day_picker.day_element("1"),
            "content-desc",
        ).seen_by(
            actor
        )  # Any day_element should give us a date object like "01 September 2024"
        fetched_month = datetime.strptime(text, "%d %B %Y").month
        return str(fetched_month)

    seen_by = answered_by
