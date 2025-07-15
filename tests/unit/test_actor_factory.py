from automate_ui.common.utils.config_manager import ConfigManager
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.ui.questions.current_url import CurrentUrl
from automate_ui.screenplay.core.ui.tasks.navigate import Navigate
from automate_ui.screenplay.core.ui.tasks.screenshot_page import ScreenshotPage


def test_actor_factory(frequent_shopper: Actor, config_manager: ConfigManager):

    frequent_shopper.attempts_to(
        Navigate.to_url(config_manager.get_url("web_app", "base_url")),
        ScreenshotPage("some_file.png"),
    )

    current_url = CurrentUrl().seen_by(frequent_shopper)
    assert current_url == "https://www.google.com/"
    assert frequent_shopper.persona.email_address
    print(frequent_shopper.persona.personal_information)
