from dataclasses import dataclass
from typing import List


@dataclass
class AdditionalInformation:
    pass


@dataclass
class Address:
    pass


@dataclass
class User:
    email_address: str = None
    password: str = None
    additional_information: AdditionalInformation = None
    address_history: List[Address]
