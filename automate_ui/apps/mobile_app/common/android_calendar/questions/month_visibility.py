from automate_ui.screenplay.core.actor import Actor
from automate_ui.apps.mobile_app.common.android_calendar.questions.selected_month import (
    SelectedMonth,
)


class MonthVisibility:
    """
    Since there is no direct Target from which we can figure out which Month is selected,
    we have to do a match based on the extracted month name from one of the date element.

    If matched, we say the Month is Visible.

    """

    def __init__(self, month_to_be_set: str):
        self.month_to_be_set = month_to_be_set

    def answered_by(self, actor: Actor) -> bool:
        fetched_month = SelectedMonth.seen_by(actor)
        return fetched_month == self.month_to_be_set

    seen_by = answered_by
