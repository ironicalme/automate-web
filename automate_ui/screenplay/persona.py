from dataclasses import dataclass, field, replace
from typing import Optional
from faker import Faker
import factory

fake = Faker()
Faker.seed(0)


@dataclass
class PersonalInformation:
    first_name: str = field(default_factory=fake.first_name)
    last_name: str = field(default_factory=fake.last_name)
    email: str = field(default_factory=fake.email)


@dataclass
class Address:
    street: str = field(default_factory=fake.street_address)
    city: str = field(default_factory=fake.city)
    state: str = field(default_factory=fake.state)
    country: str = field(default="US")
    zip_code: str = field(default_factory=fake.zipcode)


@dataclass
class BirthDetails:
    birth_date: str = field(default_factory=lambda: fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat())
    birth_place: str = field(default_factory=fake.city)


@dataclass
class User:
    personal_info: PersonalInformation
    address: Address
    birth_details: BirthDetails
    frequent_shopper: Optional[bool] = False


def get_user(**specs) -> User:
    default_user = User(
        personal_info=PersonalInformation(),
        address=Address(),
        birth_details=BirthDetails()
    )

    if "address" in specs and isinstance(specs["address"], dict):
        default_user = replace(default_user, address=replace(default_user.address, **specs["address"]))
        del specs["address"]

    if "personal_info" in specs and isinstance(specs["personal_info"], dict):
        default_user = replace(default_user, personal_info=replace(default_user.personal_info, **specs["personal_info"]))
        del specs["personal_info"]

    if "birth_details" in specs and isinstance(specs["birth_details"], dict):
        default_user = replace(default_user, birth_details=replace(default_user.birth_details, **specs["birth_details"]))
        del specs["birth_details"]

    return replace(default_user, **specs)


class PersonalInformationFactory(factory.Factory):
    class Meta:
        model = PersonalInformation

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    street = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    country = factory.LazyAttribute(lambda _: "US")
    zip_code = factory.Faker("zipcode")


class BirthDetailsFactory(factory.Factory):
    class Meta:
        model = BirthDetails

    birth_date = factory.LazyFunction(lambda: fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat())
    birth_place = factory.Faker("city")


class UserFactory(factory.Factory):
    class Meta:
        model = User

    personal_info: PersonalInformation = factory.SubFactory(PersonalInformationFactory)
    address: Address = factory.SubFactory(AddressFactory)
    birth_details: BirthDetails = factory.SubFactory(BirthDetailsFactory)
    frequent_shopper: bool = factory.Faker("boolean")
