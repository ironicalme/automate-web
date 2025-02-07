from typing import Optional, Union
import pytest

from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.actor import Actor
from automate_ui.screenplay.persona import User
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
            new_context = browse_the_web.browser.new_context(
                locale="en-US",
                # extra_http_headers={"bypass_rt": "true"},  # bypass API rate limit
                # screen=ViewportSize(width=1920, height=1080) # screensize freeze
            )
            page = new_context.new_page()
            page.set_default_timeout(timeout=timeout)
            browse_the_web.current_page = page
            browse_the_web.pages.append(page)
        return actor
    return generate_actor
