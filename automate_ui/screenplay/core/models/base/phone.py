import re

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class BasePhone(BaseModel):
    """Base phone number model with validation."""

    number: str = Field(..., description="Phone number")

    @field_validator("number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Validate phone number format."""
        # Remove any non-digit characters except +
        cleaned = re.sub(r"[^\d+]", "", v)
        if not re.match(r"^\+?\d{10,15}$", cleaned):
            raise ValueError("Phone number must be between 10 and 15 digits")
        return cleaned
