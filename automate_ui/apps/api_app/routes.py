from dataclasses import dataclass

from automate_ui.apps.common.api.routes import URL


@dataclass
class Events(URL):
    def __init__(self):
        super().__init__("events/")


@dataclass
class Order(URL):
    def __init__(self, base_url: str):
        super().__init__(base_url + "order/")


@dataclass
class Case(URL):
    def __init__(self, base_url: str, case_id: str):
        super().__init__(base_url + f"{case_id}/")


@dataclass
class Cases(URL):
    def __init__(self):
        super().__init__("cases/")

    def order(self) -> Order:
        return Order(self._url)

    def case(self, case_id) -> Case:
        return Case(self._url, case_id)


@dataclass
class Tags(URL):
    def __init__(self):
        super().__init__("tags/")


@dataclass
class Create(URL):
    def __init__(self, base_url: str):
        super().__init__(base_url + "create/")


@dataclass
class CredentialVerifier(URL):
    def __init__(self, base_url: str, credential_verifier_id: str):
        super().__init__(base_url + f"{credential_verifier_id}/")


@dataclass
class CredentialVerifiers(URL):
    def __init__(self):
        super().__init__("credential-verifiers/")

    def create(self) -> Create:
        return Create(self._url)

    def credential_verifier(self, credential_verifier_id) -> CredentialVerifier:
        return CredentialVerifier(self._url, credential_verifier_id)


@dataclass
class CredentialRequest(URL):
    def __init__(self, base_url: str, credential_request_id: str):
        super().__init__(base_url + f"{credential_request_id}/")


@dataclass
class CredentialRequests(URL):
    def __init__(self):
        super().__init__("credential-requests/")

    def create(self) -> Create:
        return Create(self._url)

    def credential_request(self, credential_request_id) -> CredentialRequest:
        return CredentialRequest(self._url, credential_request_id)


@dataclass
class AppAPI:
    cases = Cases
    events = Events
    tags = Tags
    credential_verifiers = CredentialVerifiers
    credential_requests = CredentialRequests
