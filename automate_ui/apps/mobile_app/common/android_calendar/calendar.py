from automate_ui.screenplay.core.mobile.target import LocatorStrategy, Target


class CalendarHeader:

    container = Target.the("'Calendar Header'").located_by(
        LocatorStrategy.ID, "android:id/date_picker_header"
    )

    year_picker_button = Target.the("'Year' picker on the calendar header").located_by(
        LocatorStrategy.ID, "android:id/date_picker_header_year"
    )

    displayed_date = Target.the("'Date' displayed on the calendar header").located_by(
        LocatorStrategy.ID, "android:id/date_picker_header_date"
    )


class YearPicker:

    container = Target.the("'Year picker'").located_by(
        LocatorStrategy.ID, "android:id/date_picker_year_picker"
    )

    year_elements = Target.the("All of the displayed years").located_by(
        LocatorStrategy.XPATH,
        '//android.widget.TextView[@resource-id="android:id/text1"]',
    )

    @staticmethod
    def year_element(year: str):
        return Target.the(f"Year '{year}'").located_by(
            LocatorStrategy.XPATH,
            f'//android.widget.TextView[@resource-id="android:id/text1" and @text="{year}"]',
        )


class MonthAndDayPicker:

    container = Target.the("'Month and day' picker").located_by(
        LocatorStrategy.ID, "android:id/date_picker_day_picker"
    )

    previous_month_button = Target.the("'Previous Month' button").located_by(
        LocatorStrategy.ID, "android:id/prev"
    )

    next_month_button = Target.the("'Next Month' button").located_by(
        LocatorStrategy.ID, "android:id/next"
    )

    @staticmethod
    def day_element(day: str):
        return Target.the(f"Day '{day}'").located_by(
            LocatorStrategy.XPATH, f'//android.view.View[@text="{day}"]'
        )


class AndroidCalendar:

    container = Target.the("'Calendar'").located_by(
        LocatorStrategy.ID, "android:id/parentPanel"
    )

    header = CalendarHeader
    year_picker = YearPicker
    month_and_day_picker = MonthAndDayPicker

    ok_button = Target.the("'OK' button").located_by(
        LocatorStrategy.ID, "android:id/button1"
    )

    cancel_button = Target.the("'Cancel' button").located_by(
        LocatorStrategy.ID, "android:id/button2"
    )
