from typing import List, Optional

from pydantic import BaseModel
from pydantic import Field

from ..base.address import ShortAddress
from .address import UserAddress
from .personal_information import PersonalInformation


class User(BaseModel):
    """Model representing an applicant persona."""
    personal_information: Optional[PersonalInformation] = Field(None, description="Personal information")
    addresses: Optional[List[UserAddress]] = Field(default_factory=list, description="Address history")
    email_address: Optional[str] = Field(None, description="Email address")
    password: Optional[str] = Field(None, description="Password")
    frequent_shopper: bool = Field(False, description="Frequent shopper status")


    @property
    def legal_name(self) -> str:
        """Get the applicant's legal name."""
        return self.personal_information.name.full_name

    @property
    def current_address(self) -> Optional[UserAddress]:
        """Get the applicant's current address."""
        for address in self.addresses:
            if address.current_address:
                return address
        return None