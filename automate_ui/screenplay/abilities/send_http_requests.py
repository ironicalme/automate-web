from typing import List, Optional, Tuple, Type, TypeVar

from requests import Response

from automate_ui.screenplay.core.api.rest_client import RestClient
from automate_ui.screenplay.core.exceptions import RestClientNotFoundError

T_RestClient = TypeVar("T_RestClient", bound=RestClient)


class SendHttpRequests:
    def __init__(self, rest_clients: List[RestClient]) -> None:
        self.rest_clients = rest_clients
        self.responses: List[Tuple[Optional[str], Response]] = []

    @classmethod
    def using(cls, rest_clients: list[RestClient]) -> "SendHttpRequests":
        return SendHttpRequests(rest_clients)

    def get_rest_client(self, rest_client: Type[T_RestClient]) -> T_RestClient:
        for client in self.rest_clients:
            if isinstance(client, rest_client):
                return client
        raise RestClientNotFoundError(
            f"Rest client {rest_client.__name__} was not found."
        )

    def forget(self) -> None:
        for client in self.rest_clients:
            client.session.close()
