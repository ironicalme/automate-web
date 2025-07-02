import json

from automate_ui.apps.api_app.client import APIClient
from automate_ui.apps.api_app.data.requests.users_create.payload import \
    CreateUserPayload
from automate_ui.apps.api_app.data.requests.users_create.response import \
    CreateUserResponse
from automate_ui.apps.api_app.routes import AppAPI
from automate_ui.enums.http_method import HttpMethod
from automate_ui.screenplay.abilities.send_http_requests import \
    SendHttpRequests
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.api.questions.response import Response
from automate_ui.screenplay.core.api.tasks.send_request import SendRequest
from automate_ui.screenplay.core.decorators import indent_logs


class CreateUser:
    def __init__(
        self, user_create_payload: CreateUserPayload
    ) -> None:
        self._user_create_payload = user_create_payload
        self._response: CreateUserResponse = None

    @classmethod
    def describe(cls) -> str:
        return "attempts to create a User"

    @indent_logs
    def perform(self, actor: Actor) -> None:
        api_client = actor.get_ability(SendHttpRequests).get_rest_client(
            APIClient
        )

        url = AppAPI.users().create().url

        actor.attempts_to(
            SendRequest(
                url=api_client.construct_url(url),
                method=HttpMethod.POST,
                session=api_client.session,
                json=json.loads(
                    self._user_create_payload.model_dump_json()
                ),
            )
        )

        self._response = api_client.model_response(
            CreateUserResponse,
            Response.of_latest_request().sent_by(actor),
        )

    @property
    def response(self) -> CreateUserResponse:
        return self._response
