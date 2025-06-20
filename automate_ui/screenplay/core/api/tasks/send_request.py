from typing import Any

import requests

from automate_ui.enums.http_method import HttpMethod
from automate_ui.screenplay.abilities.send_http_requests import SendHttpRequests
from automate_ui.screenplay.core.actor import Actor


class SendRequest:
    """
    Sends an HTTP request with the requests library using the actor's active Session.
    If the URL passed in is partial, this task will automatically combine it with a base_url (if it exists).

    Examples
        actor.attempts_to(
            SendRequest(
                session=session,
                method=HttpMethods.GET,
                url="https://www.google.com"
            )
        )

        actor.attempts_to(
            SendRequest(
                session=session,
                method=HttpMethods.POST,
                url=some_base_url + Routes.api.login
            )
        )

        actor.attempts_to(
            SendRequest(
                session=session,
                method=HttpMethods.POST,
                url=Routes.hr.applications.invite,
                json={"request_identity_verification": True}
            ).saved_as("send_invite_application_response")
        )
    """

    def __init__(
        self,
        method: HttpMethod,
        url: str,
        session: requests.Session,
        **kwargs: Any,
    ):
        self.url = url
        self.session = session
        self.method = method
        self.kwargs = kwargs
        self.name = None

    def saved_as(self, name: str = None):
        """
        Saves a request for future retrieval in the SendHttpRequests Ability
        Note: In cases of duplicate names, the first one saved will be retrieved
        """
        self.name = name
        return self

    def describe(self) -> str:
        return f"sends a {self.method.value} request to:\n    {self.url}"

    def perform(self, actor: Actor) -> None:

        send_http_requests_ability = actor.get_ability(SendHttpRequests)

        http_requests = {
            HttpMethod.GET: self.session.get,
            HttpMethod.PUT: self.session.put,
            HttpMethod.POST: self.session.post,
            HttpMethod.PATCH: self.session.patch,
            HttpMethod.DELETE: self.session.delete,
        }

        if "{" in self.url or "}" in self.url:
            raise Exception(
                f"placeholder values were not overridden in url\n{self.url}"
            )

        response = http_requests[self.method](self.url, **self.kwargs)
        send_http_requests_ability.responses.append((self.name, response))
