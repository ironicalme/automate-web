from datetime import datetime
from typing import Optional

from pydantic import Field

from ..base.address import BaseAddress


class UserAddress(BaseAddress):
    """Address model with date fields and current address flag."""

    start_date: datetime = Field(..., description="Start date of residence")
    end_date: Optional[datetime] = None
    current_address: bool = Field(
        default=False, description="Whether this is the current address"
    )

    @property
    def start_date_day(self) -> str:
        return str(self.start_date.day)

    @property
    def start_date_month(self) -> str:
        return str(self.start_date.month)

    @property
    def start_date_year(self) -> str:
        return str(self.start_date.year)

    @property
    def end_date_day(self) -> Optional[str]:
        return str(self.end_date.day) if self.end_date else None

    @property
    def end_date_month(self) -> Optional[str]:
        return str(self.end_date.month) if self.end_date else None

    @property
    def end_date_year(self) -> Optional[str]:
        return str(self.end_date.year) if self.end_date else None
