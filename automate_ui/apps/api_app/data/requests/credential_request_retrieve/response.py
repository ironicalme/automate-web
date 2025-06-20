from typing import Any, Dict, List, Optional

from automate_ui.apps.api_app.data.requests.common import response


class HolderData(response.APIResponse):
    email: str
    given_name: str
    family_name: str
    phone_number: Optional[str]


class CredentialRequestsRetrieveResponse(response.APIResponse):
    id: str
    created: str
    status: str
    requested_credential_types: List[str]
    verifier_id: str
    defer_availability: bool
    holder_data: HolderData
    custom_message: str
    credentials_data: Dict[str, Any]
