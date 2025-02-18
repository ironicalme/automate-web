from re import Pattern
from typing import Any, Dict, Union

from automate_ui.screenplay.abilities import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor


class ExpectResponse:

    def __init__(self, url_path_or_regex: Union[str, Pattern]):
        self._url_path_or_regex: Union[str, Pattern] = url_path_or_regex

    @classmethod
    def from_url(cls, url: str) -> "ExpectResponse":
        return ExpectResponse(url)

    @classmethod
    def from_url_regex(cls, url_regex: Pattern) -> "ExpectResponse":
        return ExpectResponse(url_regex)

    def answered_by(self, actor: Actor) -> Dict[str, Any]:
        current_page = actor.get_ability(BrowseTheWeb).current_page
        with current_page.expect_response(self._url_path_or_regex) as response:
            try:
                json = response.value.json()
            except Exception as e:
                raise e
        return dict(json)

    requested_by = answered_by
