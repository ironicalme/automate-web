# import pytest
from automate_ui.screenplay.core.models.user.generate_user import GenerateUserPersona


def test_generate_random_user():
    """Test that get_user() generates a random user with default values."""
    user = (
        GenerateUserPersona()
        .with_personal_info(phone_country="Canada")
        .with_address(country="Canada")
        .with_personal_info()
        .with_email()
        .with_password()
        .build()
    )

    print(f"{user}")
    assert user.personal_information.given_name
    assert user.addresses[0].country == "Canada"
    assert isinstance(user.frequent_shopper, bool)
