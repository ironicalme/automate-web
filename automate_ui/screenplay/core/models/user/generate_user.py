from typing import List, Optional
from datetime import datetime, timedelta, date
from faker import Faker


from ..base.name import BaseName
from ..base.phone import BasePhone
from ..base.faker_providers import CountrySpecificProvider, PhoneNumberGenerator
from .address import UserAddress
from .personal_information import PersonalInformation, BirthLocation
from .user import User

class GenerateUserPersona:
    """Builder for creating user personas with a fluent interface."""

    def __init__(self):
        self.faker = Faker()
        self.faker.add_provider(CountrySpecificProvider)
        self._personal_info: Optional[PersonalInformation] = None
        self._addresses: List[UserAddress] = []
        self._email_address: Optional[str] = None
        self._password: Optional[str] = None
        self._frequent_shopper: bool = False


    def _calculate_address_dates(self, months_ago: int, duration_in_months: int) -> tuple[datetime, Optional[datetime]]:
        """Calculate start and end dates for an address.

        Args:
            months_ago: How many months ago the address started
            duration_in_months: How long the address lasted

        Returns:
            Tuple of (start_date, end_date)
        """
        end_date = datetime.now() - timedelta(days=months_ago * 30)
        start_date = end_date - timedelta(days=duration_in_months * 30)

        # Set day to 1 for both dates
        start_date = start_date.replace(day=1)
        end_date = end_date.replace(day=1)

        return start_date, end_date

    def with_address(
        self,
        country: str,
        is_current: bool = False,
        months_ago: Optional[int] = 6,
        duration_in_months: Optional[int] = 6
    ) -> 'GenerateUserPersona':
        """Add an address to the user's history.

        Args:
            country: The country for the address
            is_current: Whether this is the current address
            months_ago: How many months ago the address started
            duration_in_months: How long the address lasted (ignored if is_current is True)
        """
        # Calculate dates
        start_date, end_date = self._calculate_address_dates(
            months_ago=months_ago,
            duration_in_months=duration_in_months if not is_current else 0
        )

        # Generate country-specific address data
        address = UserAddress(
            country=country,
            administrative_division=self.faker.country_state(country),
            locality=self.faker.city(),
            county=self.faker.county() if country in ("United States", "United Kingdom") else None,
            unit=str(self.faker.random_number(digits=3)),
            address=self.faker.street_address(),
            postal_code=self.faker.country_postal_code(country),
            start_date=start_date,
            end_date=None if is_current else end_date,
            current_address=is_current
        )

        self._addresses.append(address)
        return self

    def with_personal_info(
        self,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        additional_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        phone_country: str = "Canada",
        date_of_birth: Optional[date] = None,
        country_of_birth: Optional[str] = None,
        state_of_birth: Optional[str] = None,
        city_of_birth: Optional[str] = None,
        sin: Optional[str] = None,
    ) -> 'GenerateUserPersona':
        """Set the user's personal information."""
        name = BaseName(
            given_name=given_name or self.faker.first_name(),
            family_name=family_name or self.faker.last_name(),
            additional_name=additional_name or self.faker.name()
        )
        phone = BasePhone(
            number=phone_number or PhoneNumberGenerator.generate_phone_number(self.faker, phone_country)
        )
        birth_date = date_of_birth or self.faker.date_of_birth(minimum_age=18, maximum_age=80)
        birth_location = BirthLocation(
            country=country_of_birth or phone_country,  # Use phone country as default birth country
            administrative_division=state_of_birth or self.faker.country_state(country_of_birth or phone_country),
            locality=city_of_birth or self.faker.city()
        )
        self._personal_info = PersonalInformation(
            name=name,
            phone=phone,
            date_of_birth=birth_date,
            birth_location=birth_location,
            sin=sin or str(self.faker.random_number(digits=9)),
        )
        return self

    def with_email(self, email: Optional[str] = None) -> 'GenerateUserPersona':
        """Set the applicant's email."""
        if email:
            self._email_address = email
        else:
            # Generate random 6 character string
            random_str = self.faker.random_letters(6)
            # Get first and last name from personal info if available
            if self._personal_info:
                given_name = self._personal_info.name.given_name.lower()
                family_name = self._personal_info.name.family_name.lower()
                self._email_address = f"{given_name}_{family_name}_{random_str}@companyinbox.com"
            else:
                # Fallback to random names if personal info not set
                first_name = self.faker.first_name().lower()
                last_name = self.faker.last_name().lower()
                self._email_address = f"{first_name}_{last_name}_{random_str}@companyinbox.com"
        return self

    def with_password(self, password: Optional[str] = None) -> 'GenerateUserPersona':
        """Set the user's password.

        Args:
            password: Optional password. If not provided, generate a random one.
        """
        if not password:
            password = self.faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        # Add conditions if fetching password from valut/aws

        self._password = password
        return self

    def build(self) -> User:
        """Build and return the user persona."""
        return User(
            personal_information=self._personal_info,
            addresses=self._addresses,
            email_address=self._email_address,
            password=self._password,
            frequent_shopper=self._frequent_shopper
        )
