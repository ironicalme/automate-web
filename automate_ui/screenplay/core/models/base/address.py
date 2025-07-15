from typing import Optional

import pycountry
from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class ShortAddress(BaseModel):
    """Base model for location information with country, administrative division (province/state/territory), and locality (city/town)."""

    country: str = Field(..., description="Country name")
    country_code: Optional[str] = None
    administrative_division: str = Field(..., description="Province/state/territory")
    administrative_division_code: Optional[str] = None
    locality: str = Field(..., description="City/town")

    @model_validator(mode="after")
    def set_codes(self) -> "ShortAddress":
        """Set country and administrative division codes based on names."""
        if self.country:
            country = pycountry.countries.get(name=self.country)
            if country:
                self.country_code = country.alpha_2

                if self.administrative_division:
                    subdivisions = pycountry.subdivisions.get(
                        country_code=self.country_code
                    )
                    if subdivisions:
                        for subdivision in list(subdivisions):
                            if self.administrative_division in subdivision.name:
                                self.administrative_division_code = str(
                                    subdivision.code
                                ).replace(f"{self.country_code}-", "")
                                break
        return self


class BaseAddress(ShortAddress):
    """Full address model with all address fields."""

    address: str = Field(..., description="Street address")
    unit: Optional[str] = None
    county: Optional[str] = None
    postal_code: str = Field(..., description="Postal/ZIP code")
