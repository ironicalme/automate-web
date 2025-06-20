from typing import List, Optional

from pydantic import BaseModel

from automate_ui.screenplay.core.actor import T_Persona
from automate_ui.enums.credential_types import CredentialTypes



class CreateCredentialRequestPayload(BaseModel):
    verifier: str
    types: List[str]
    holder_email: str
    holder_given_name: Optional[str] = None
    holder_family_name: Optional[str] = None
    holder_phone_number: Optional[str] = None
    holder_consent_obtained: bool = True
    custom_message: Optional[str] = None
    defer_availability: bool = False


class CreateCredentialRequestPayloadFactory:
    """

    A factory class to build and generate a `CreateCredentialRequestPayload` object.

    Methods:
        `with_verifier(verifier: str) -> Self:`
            Sets the verifier ID.
        `with_credential_types(types: List[str]) -> Self:`
            Sets the list of credential types.
        `for_holder(holder: T_Persona) -> Self:`
            Populates holder information using a `T_Persona` object.
        `with_custom_message(custom_message: str) -> Self:`
            Sets a custom message for the payload.
        `defer_credential_when_available(defer_availability: bool) -> Self:`
            Sets whether to defer the credential's availability.
        `consent_obtained(holder_consent_obtained: bool) -> Self:`
            Indicates whether the holder's consent has been obtained.
        `generate_payload() -> CreateCredentialRequestPayload:`
            Generates and returns a `CreateCredentialRequestPayload` object.
            Raises:
                `ValueError`: If mandatory fields (`verifier`, `types`, or `holder_email`)
                are missing.

    """

    def __init__(self) -> None:
        self.verifier: str = None
        self.types: List[CredentialTypes] = None
        self.holder_email = ""
        self.holder_consent_obtained = False
        self.defer_availability: bool = False
        self.custom_message: str = None

    def with_verifier(self, verifier: str):
        self.verifier = verifier
        return self

    def with_credential_types(self, types: List[CredentialTypes]):
        self.types = types
        return self

    def for_holder(self, holder: T_Persona):
        self.holder_email = holder.email_address
        self.holder_given_name = holder.personal_information.given_name
        self.holder_family_name = holder.personal_information.family_name
        self.holder_phone_number = holder.personal_information.phone_number
        return self

    def with_custom_message(self, custom_message: str):
        self.custom_message = custom_message
        return self

    def defer_credential_when_available(self, defer_availability: bool):
        self.defer_availability = defer_availability
        return self

    def consent_obtained(self, holder_consent_obtained: bool):
        self.holder_consent_obtained = holder_consent_obtained
        return self

    def generate_payload(self) -> CreateCredentialRequestPayload:
        if not self.verifier:
            raise ValueError(
                "Verifier's ID is required. Use `with_verifier()` method to pass in verifier's ID"
            )
        if not self.types:
            raise ValueError(
                "Atleast one Credential type is required. Use `with_credential_type()` to set it"
            )
        if not self.holder_email:
            raise ValueError(
                "Holder's email is required. Use `for_holder()` to pass it in"
            )
        credential_types = [
            credential_type.in_pascal_case for credential_type in self.types
        ]
        return CreateCredentialRequestPayload(
            verifier=self.verifier,
            types=credential_types,
            holder_consent_obtained=self.holder_consent_obtained,
            holder_email=self.holder_email,
            holder_given_name=self.holder_given_name,
            holder_family_name=self.holder_family_name,
            holder_phone_number=self.holder_phone_number,
            custom_message=self.custom_message,
            defer_availability=self.defer_availability,
        )
