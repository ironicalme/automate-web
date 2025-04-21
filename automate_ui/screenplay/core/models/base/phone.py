from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class BasePhone(BaseModel):
    """Base phone number model with validation."""
    number: str = Field(..., description="Phone number")

    @field_validator('number')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Validate phone number format."""
        # Remove any non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', v)
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError('Phone number must be between 10 and 15 digits')
        return cleaned
