from automate_ui.apps.api_app.client import APIClient
from automate_ui.apps.api_app.data.requests.fetch_user.response import \
    FetchUserResponse
from automate_ui.apps.api_app.routes import AppAPI
from automate_ui.enums.http_method import HttpMethod
from automate_ui.screenplay.abilities.send_http_requests import \
    SendHttpRequests
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.api.questions.response import Response
from automate_ui.screenplay.core.api.tasks.send_request import SendRequest


class FetchUser:
    def __init__(self, id: str):
        self._id = id

    @classmethod
    def matching(cls, id: str) -> "FetchUser":
        return FetchUser(id)

    def answered_by(self, actor: Actor):
        api_client = actor.get_ability(SendHttpRequests).get_rest_client(
            APIClient
        )

        actor.narrate(
            f"{actor} attempts to retrieve user with id={self._id}"
        )

        url = AppAPI.users().user(self._id).url

        actor.attempts_to(
            SendRequest(
                method=HttpMethod.GET,
                url=api_client.construct_url(url),
                session=api_client.session,
            )
        )

        return api_client.model_response(
            FetchUserResponse,
            Response.of_latest_request().sent_by(actor),
        )

    requested_by = answered_by
