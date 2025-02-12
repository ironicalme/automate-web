from typing import Optional, Union
import pytest

from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.actor import Actor
from automate_ui.screenplay.persona import User, UserFactory
from automate_ui.screenplay.tasks.screenshot_page import ScreenshotPage
# from playwright._impl._api_structures import ViewportSize


@pytest.fixture(scope='class')
def actor_factory():
    def generate_actor(
        name: str,
        abilities,
        persona: Optional[Union["User"]] = None,  # Add more Personas as required
        timeout: Optional[int] = 1000 * 60
    ) -> Actor:
        actor = Actor(name=name)
        actor.add_abilities(*abilities)
        actor.persona = persona
        if actor.has_ability(BrowseTheWeb):
            browse_the_web = actor.get_ability(BrowseTheWeb)
            page = browse_the_web.browser.new_page()
            # new_context = browse_the_web.browser.new_context(
            #     locale="en-US",
            #     # extra_http_headers={"bypass_rt": "true"},  # bypass API rate limit
            #     # screen=ViewportSize(width=1920, height=1080) # screensize freeze
            # )
            # page = new_context.new_page()
            page.set_default_timeout(timeout=timeout)
            browse_the_web.current_page = page
            browse_the_web.pages.append(page)
        return actor
    return generate_actor


@pytest.fixture
def frequent_shopper(
    playwright,
    actor_factory,
    take_screenshot_on_test_failure
) -> Actor:
    persona = UserFactory(frequent_shopper=True)

    user = actor_factory(
        name=persona.personal_info.first_name,
        abilities=(
            BrowseTheWeb.using_chromium(playwright),
            # Add more abilities as requred
        ),
        persona=persona
    )

    yield user

    take_screenshot_on_test_failure(user)

    user.cleanup()


@pytest.fixture
def take_screenshot_on_test_failure(request):
    def take_screenshot(actor: Actor):

        actor_involved_in_failed_test = request.node.rep_setup.failed or request.node.rep_call.failed

        if actor_involved_in_failed_test:
            partial_path = f"{request.node.name}/{actor.name.replace(' ', '-').lower()}/screenshot.png"
            actor.attempts_to(ScreenshotPage.saved_as(file_name=partial_path, file_type="png"))
    return take_screenshot
