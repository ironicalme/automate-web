from automate_ui.screenplay.core.mobile.target import LocatorStrategy, Target


class DatePickerWheel:
    container = Target.the("'Date Picker' wheel").located_by(
        LocatorStrategy.XPATH,
        '//XCUIElementTypeDatePicker[contains(@name, "form--DateFieldControl")]',
    )

    selected_month = Target.the(
        "currently selected/displayed month on the Month Picker wheel"
    ).located_by(LocatorStrategy.XPATH, "//XCUIElementTypePickerWheel[1]")

    selected_day = Target.the(
        "currently selected/displayed day on the Day Picker wheel"
    ).located_by(LocatorStrategy.XPATH, "//XCUIElementTypePickerWheel[2]")

    selected_year = Target.the(
        "currently selected/displayed year on the Year Picker wheel"
    ).located_by(LocatorStrategy.XPATH, "//XCUIElementTypePickerWheel[3]")

    done_button = Target.the("'Done' button of date wheel").located_by(
        LocatorStrategy.XPATH,
        '//XCUIElementTypeButton[@name="button" and @label="Done"]',
    )
