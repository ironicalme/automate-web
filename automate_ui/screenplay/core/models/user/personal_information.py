from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from ..base.address import ShortAddress
from ..base.name import BaseName
from ..base.phone import BasePhone


class BirthLocation(ShortAddress):
    """Birth location information using standardized location fields."""

    pass


class PersonalInformation(BaseModel):
    """Model combining registration and personal information."""

    name: BaseName = Field(..., description="User's name")
    phone: BasePhone = Field(..., description="User's phone number")
    date_of_birth: date = Field(..., description="Date of birth")
    birth_location: BirthLocation = Field(..., description="Birth location details")
    agree_to_privacy_policy: bool = Field(
        default=True, description="Privacy policy agreement"
    )
    subscribe_to_mailing_list: bool = Field(
        default=False, description="Marketing subscription opt-in"
    )
    sin: Optional[str] = Field(None, description="Social Insurance Number (Canada)")

    @property
    def day(self) -> str:
        return str(self.date_of_birth.day)

    @property
    def month(self) -> str:
        return str(self.date_of_birth.month)

    @property
    def year(self) -> str:
        return str(self.date_of_birth.year)

    @property
    def country_of_birth(self) -> str:
        return self.birth_location.country

    @property
    def country_code(self) -> Optional[str]:
        return self.birth_location.country_code

    @property
    def state_of_birth(self) -> str:
        return self.birth_location.administrative_division

    @property
    def province_state_code(self) -> Optional[str]:
        return self.birth_location.administrative_division_code

    @property
    def city(self) -> str:
        return self.birth_location.locality

    @property
    def given_name(self) -> str:
        return self.name.given_name

    @property
    def family_name(self) -> str:
        return self.name.family_name

    @property
    def additional_name(self) -> Optional[str]:
        return self.name.additional_name

    @property
    def phone_number(self) -> str:
        return self.phone.number
