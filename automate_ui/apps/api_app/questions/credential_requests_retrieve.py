from automate_ui.apps.api_app.data.requests.credential_request_retrieve.response import CredentialRequestsRetrieveResponse
from automate_ui.enums.http_method import HttpMethod
from automate_ui.screenplay.abilities.send_http_requests import SendHttpRequests
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.api.questions.response import Response
from automate_ui.screenplay.core.api.tasks.send_request import SendRequest
from automate_ui.apps.api_app.client import APIClient
from automate_ui.apps.api_app.routes import AppAPI



class CredentialRequestsRetrieve:
    def __init__(self, id: str):
        self._id = id

    @classmethod
    def matching(cls, id: str) -> "CredentialRequestsRetrieve":
        return CredentialRequestsRetrieve(id)

    def answered_by(self, actor: Actor):
        public_api_client = actor.get_ability(SendHttpRequests).get_rest_client(
            APIClient
        )

        actor.narrate(
            f"{actor} attempts to retrieve credentialrequest with id={self._id}"
        )

        url = AppAPI.credential_requests().credential_request(self._id).url

        actor.attempts_to(
            SendRequest(
                method=HttpMethod.GET,
                url=public_api_client.construct_url(url),
                session=public_api_client.session,
            )
        )

        return public_api_client.model_response(
            CredentialRequestsRetrieveResponse,
            Response.of_latest_request().sent_by(actor),
        )

    requested_by = answered_by
