from pydantic import BaseModel

from automate_ui.screenplay.core.models.user.personal_information import \
    PersonalInformation


class CreateUserPayload(BaseModel):
    email_address: str
    password: str
    frequent_shopper: bool = False
    personal_information: PersonalInformation


class CreateUserPayloadFactory:
    """

    A factory class to build and generate a `CreateUserPayload` object.

    Methods:
        `with_email_address(email_address: str) -> Self:`
            Sets the email address.
        `with_password(password: str) -> Self:`
            Sets the password.
        `with_frequent_shopper(frequent_shopper: bool) -> Self:`
            Sets the frequent shopper status.
        `with_personal_information(personal_information: PersonalInformation) -> Self:`
            Sets the personal information.
        `generate_payload() -> CreateUserPayload:`
            Generates and returns a `CreateUserPayload` object.
            Raises:
                `ValueError`: If mandatory fields (`email_address`, `password`, or `personal_information`)
                are missing.

    """

    def __init__(self) -> None:
        self.email_address: str = None
        self.password: str = None
        self.frequent_shopper: bool = False
        self.personal_information: PersonalInformation = None

    def with_email_address(self, email_address: str):
        self.email_address = email_address
        return self

    def with_password(self, password: str):
        self.password = password
        return self

    def with_personal_information(self, personal_information: PersonalInformation):
        self.personal_information = personal_information
        return self

    def with_frequent_shopper(self, frequent_shopper: bool):
        self.frequent_shopper = frequent_shopper
        return self

    def generate_payload(self) -> CreateUserPayload:
        if not self.email_address:
            raise ValueError(
                "Email address is required. Use `with_email_address()` method to pass in email address"
            )
        if not self.password:
            raise ValueError(
                "Password is required. Use `with_password()` method to pass in password"
            )
        if not self.personal_information:
            raise ValueError(
                "Personal information is required. Use `with_personal_information()` to pass it in"
            )
        return CreateUserPayload(
            email_address=self.email_address,
            password=self.password,
            frequent_shopper=self.frequent_shopper,
            personal_information=self.personal_information,
        )
