import time

from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.questions.current_url import CurrentUrl
from automate_ui.screenplay.core.ui.tasks.navigate import Navigate
from automate_ui.screenplay.core.ui.tasks.screenshot_page import ScreenshotPage


def test_actor_factory(
    frequent_shopper: Actor
):

    frequent_shopper.attempts_to(
        Navigate.to_url("https://www.google.com/"),
        ScreenshotPage("some_file.png")
    )

    current_url = CurrentUrl().seen_by(frequent_shopper)
    assert current_url == "https://www.google.com/"
    # assert frequent_shopper.persona.email_address
    print(frequent_shopper.persona.personal_information)
