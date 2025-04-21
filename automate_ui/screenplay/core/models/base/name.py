from typing import Optional
from pydantic import BaseModel, Field


class BaseName(BaseModel):
    """Base name model with common fields and validation."""
    given_name: str = Field(..., description="First/given name")
    family_name: str = Field(..., description="Last/family name")
    additional_name: Optional[str] = None

    @property
    def full_name(self) -> str:
        """Get the full name including additional name if present."""
        parts = [self.given_name]
        if self.additional_name:
            parts.append(self.additional_name)
        parts.append(self.family_name)
        return " ".join(parts)