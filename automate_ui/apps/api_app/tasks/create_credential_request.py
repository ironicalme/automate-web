import json

from automate_ui.enums.http_method import HttpMethod
from automate_ui.screenplay.abilities.send_http_requests import SendHttpRequests
from automate_ui.screenplay.core.actor import Actor
from automate_ui.apps.api_app.client import APIClient
from automate_ui.apps.api_app.data.requests.credential_requests_create.payload import (
    CreateCredentialRequestPayload,
)
from automate_ui.apps.api_app.data.requests.credential_requests_create.response import (
    CreateCredentialRequestResponse,
)
from automate_ui.apps.api_app.routes import AppAPI
from automate_ui.screenplay.core.decorators import indent_logs
from automate_ui.screenplay.core.api.questions.response import Response
from automate_ui.screenplay.core.api.tasks.send_request import SendRequest


class CreateCredentialRequest:
    def __init__(
        self, credential_request_create_payload: CreateCredentialRequestPayload
    ) -> None:
        self._credential_request_create_payload = credential_request_create_payload
        self._response: CreateCredentialRequestResponse = None

    @classmethod
    def describe(cls) -> str:
        return "attempts to create a Credential request"

    @indent_logs
    def perform(self, actor: Actor) -> None:
        public_api_client = actor.get_ability(SendHttpRequests).get_rest_client(
            APIClient
        )

        url = AppAPI.credential_requests().create().url

        actor.attempts_to(
            SendRequest(
                url=public_api_client.construct_url(url),
                method=HttpMethod.POST,
                session=public_api_client.session,
                json=json.loads(
                    self._credential_request_create_payload.model_dump_json()
                ),
            )
        )

        self._response = public_api_client.model_response(
            CreateCredentialRequestResponse,
            Response.of_latest_request().sent_by(actor),
        )

    @property
    def response(self) -> CreateCredentialRequestResponse:
        return self._response
