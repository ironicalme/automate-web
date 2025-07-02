from typing import List, Optional

from automate_ui.apps.api_app.data.requests.common import response


class PersonalInformation(response.APIResponse):
    given_name: str
    family_name: str
    phone_number: Optional[str]


class FetchUserResponse(response.APIResponse):
    id: str
    created: str
    status: str
    personal_information: PersonalInformation
    email_address: str
    frequent_shopper: bool


class FetchUserListResponse(response.APIPaginatedResponse):
    results: List[FetchUserResponse]