from datetime import date
from datetime import datetime

from automate_ui.apps.mobile_app.common.android_calendar import AndroidCalendar
from automate_ui.apps.mobile_app.common.android_calendar import (
    MonthVisibility as AndroidMonthVisibility,
)
from automate_ui.apps.mobile_app.common.android_calendar import (
    SelectedMonth as AndroidSelectedMonth,
)
from automate_ui.apps.mobile_app.common.android_calendar import (
    YearVisibility as AndroidYearVisibility,
)
from automate_ui.apps.mobile_app.common.constants import MAX_SCROLL_ATTEMPTS
from automate_ui.apps.mobile_app.common.ios_date_picker_wheel import DatePickerWheel
from automate_ui.apps.mobile_app.common.ios_date_picker_wheel import SelectedDay
from automate_ui.apps.mobile_app.common.ios_date_picker_wheel import (
    SelectedMonth as IOSSelectedMonth,
)
from automate_ui.apps.mobile_app.common.ios_date_picker_wheel import SelectedYear
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.tasks.click import Click
from automate_ui.screenplay.core.mobile.tasks.common import BaseTask
from automate_ui.screenplay.core.mobile.tasks.common import register_task
from automate_ui.screenplay.core.mobile.tasks.common import TaskPerformer
from automate_ui.screenplay.core.mobile.tasks.scroll import Scroll
from automate_ui.screenplay.core.mobile.tasks.tap import Tap


class SelectDate(TaskPerformer):
    """
    Common Task to Select given date from the date Picker Wheel for Ios and Calendar for Android.

    Args:
        year, month and day. Ex. "2024", "12", "31"

    Usage:
    actor.attempts_to(
        SelectDate(self.birth_info.year, self.birth_info.month, self.birth_info.day)
    )
    """

    def __init__(self, year, month, day) -> None:
        super().__init__(SelectDate, year=year, month=month, day=day)


@register_task(SelectDate, "android")
class AndroidSelectDate(BaseTask):

    def __init__(self, year: str, month: str, day: str) -> None:
        self.year = year
        self.month = month
        self.day = day

    def describe(self) -> str:
        return f"attempts to select Year: {self.year}, Month: {self.month} \
        and day: {self.day} from the Android Calendar"

    def perform(self, actor: Actor):
        current_year = date.today().year
        gap = 6  # Standard number of years displayed in Android Calendar.
        scroll_start_year = current_year - gap
        scroll_end_year = current_year

        actor.attempts_to(Click(AndroidCalendar.header.year_picker_button))

        # Set year
        scroll_attempt = 0
        while (
            AndroidYearVisibility(self.year).seen_by(actor) is False
            and scroll_attempt < MAX_SCROLL_ATTEMPTS
        ):
            actor.attempts_to(
                Scroll()
                .down()
                .from_element(
                    AndroidCalendar.year_picker.year_element(str(scroll_start_year))
                )
                .to_element(
                    AndroidCalendar.year_picker.year_element(str(scroll_end_year))
                )
                .with_speed(1000)
            )
            scroll_attempt += 1
            scroll_start_year = scroll_start_year - gap
            scroll_end_year = scroll_start_year + gap
            if scroll_attempt == MAX_SCROLL_ATTEMPTS:
                raise RuntimeError(f"Year {self.year} not visible after scrolling")

        actor.attempts_to(Click(AndroidCalendar.year_picker.year_element(self.year)))

        # Set month
        scroll_attempt = 0
        while (
            AndroidMonthVisibility(self.month).seen_by(actor) is False
            and scroll_attempt < MAX_SCROLL_ATTEMPTS
        ):
            if AndroidSelectedMonth.seen_by(actor) < self.month:
                actor.attempts_to(
                    Click(AndroidCalendar.month_and_day_picker.next_month_button)
                )
            else:
                actor.attempts_to(
                    Click(AndroidCalendar.month_and_day_picker.previous_month_button)
                )
            scroll_attempt += 1
            if scroll_attempt == MAX_SCROLL_ATTEMPTS:
                raise RuntimeError(f"Month {self.month} not visible after scrolling")

        # Set day
        actor.attempts_to(
            Click(AndroidCalendar.month_and_day_picker.day_element(self.day)),
            Click(AndroidCalendar.ok_button),
        )


@register_task(SelectDate, "ios")
class IosSelectDate(BaseTask):
    def __init__(self, year: str, month: str, day: str) -> None:
        self.year = year
        self.month = month
        self.day = day

    def describe(self) -> str:
        return f"attempts to select Month: {self.month}, day: {self.day} \
        and Year: {self.year} from the iOS date picker wheel"

    def perform(self, actor: Actor):

        def _calculate_step_and_direction(current_index, target_index, total_items):
            """
            Calculate the step size and direction for scrolling.

            :param current_index: Index of the currently visible item.
            :param target_index: Index of the desired item.
            :param total_items: Total number of items in the list.
            :return: Tuple containing step size and direction ('up' or 'down').
            """
            diff = target_index - current_index
            if abs(diff) <= total_items // 2:  # Shorter distance in one direction
                step = abs(diff)
                direction = "up" if diff > 0 else "down"
            else:  # Shorter distance by wrapping around
                step = total_items - abs(diff)
                direction = "down" if diff > 0 else "up"
            return min(step, 20), direction  # Limit the step to a maximum of 20

        # Set year
        years = [str(year) for year in range(1900, 2101)]
        target_year = str(self.year)

        scroll_attempt = 0
        while (
            SelectedYear.seen_by(actor) != target_year
            and scroll_attempt < MAX_SCROLL_ATTEMPTS
        ):
            displayed_year_index = years.index(SelectedYear.seen_by(actor))
            target_year_index = years.index(target_year)

            step, direction = _calculate_step_and_direction(
                displayed_year_index, target_year_index, len(years)
            )
            if step == 0:
                break

            if step >= 10:
                scroll_action = (
                    Scroll().flick().from_element(DatePickerWheel.selected_year)
                )
            else:
                scroll_action = (
                    Scroll()
                    .within(DatePickerWheel.selected_year)
                    .step(step)
                    .from_element(DatePickerWheel.selected_year)
                )
            actor.attempts_to(
                scroll_action.up() if direction == "up" else scroll_action.down()
            )
            scroll_attempt += 1
            if scroll_attempt == MAX_SCROLL_ATTEMPTS:
                raise RuntimeError(f"Year {self.year} not visible after scrolling")

        actor.narrate(f"{SelectedYear.seen_by(actor)} is displayed")
        actor.attempts_to(Tap(DatePickerWheel.selected_year))

        # Set month
        target_month = datetime.strptime(self.month, "%m").strftime("%B")

        scroll_attempt = 0
        while (
            IOSSelectedMonth.seen_by(actor) != target_month
            and scroll_attempt < MAX_SCROLL_ATTEMPTS
        ):
            displayed_month_index = (
                datetime.strptime(IOSSelectedMonth.seen_by(actor), "%B").month - 1
            )
            target_month_index = int(self.month) - 1

            # Calculate step and direction
            step, direction = _calculate_step_and_direction(
                displayed_month_index, target_month_index, 12
            )
            if step == 0:
                break

            # Scroll action
            scroll_action = (
                Scroll()
                .within(DatePickerWheel.selected_month)
                .step(step)
                .from_element(DatePickerWheel.selected_month)
            )

            actor.attempts_to(
                scroll_action.up() if direction == "up" else scroll_action.down()
            )
            scroll_attempt += 1

            if scroll_attempt == MAX_SCROLL_ATTEMPTS:
                raise RuntimeError(f"Month {self.year} not visible after scrolling")

        actor.narrate(f"{IOSSelectedMonth.seen_by(actor)} is displayed")
        actor.attempts_to(Tap(DatePickerWheel.selected_month))

        # Set day
        days = [str(day) for day in range(1, 32)]
        target_day = str(self.day)

        scroll_attempt = 0
        while (
            SelectedDay.seen_by(actor) != target_day
            and scroll_attempt < MAX_SCROLL_ATTEMPTS
        ):
            displayed_day_index = days.index(SelectedDay.seen_by(actor))
            target_day_index = days.index(target_day)

            step, direction = _calculate_step_and_direction(
                displayed_day_index, target_day_index, len(days)
            )
            if step == 0:
                break

            if step >= 10:
                scroll_action = (
                    Scroll().flick().from_element(DatePickerWheel.selected_day)
                )
            else:
                scroll_action = (
                    Scroll()
                    .within(DatePickerWheel.selected_day)
                    .step(step)
                    .from_element(DatePickerWheel.selected_day)
                )

            actor.attempts_to(
                scroll_action.up() if direction == "up" else scroll_action.down()
            )
            scroll_attempt += 1

            if scroll_attempt == MAX_SCROLL_ATTEMPTS:
                raise RuntimeError(f"Day {self.day} not visible after scrolling")

        actor.narrate(f"{SelectedDay.seen_by(actor)} is displayed")
        actor.attempts_to(Tap(DatePickerWheel.selected_day))

        actor.attempts_to(Click(DatePickerWheel.done_button))
