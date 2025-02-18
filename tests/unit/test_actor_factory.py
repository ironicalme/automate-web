import time
from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.tasks.navigate import Navigate


def test_actor_factory(
    frequent_shopper: Actor
):

    frequent_shopper.attempts_to(
        Navigate.to_url("https://www.google.com/")
    )
    page = frequent_shopper.get_ability(BrowseTheWeb).current_page
    assert page.url == "https://www.google.com/"
    assert frequent_shopper.persona.personal_info.email

    time.sleep(10)
