# import pytest
from automate_ui.screenplay.core.persona import User, UserFactory


def test_generate_random_user():
    """Test that get_user() generates a random user with default values."""
    user = User.get_user()
    print(f"{user}")
    assert user.personal_info.first_name
    assert user.address.country == "US"
    assert isinstance(user.frequent_shopper, bool)


def test_generate_user_with_specs():
    """Test that get_user() correctly overrides specified values."""
    user = User.get_user(frequent_shopper=True, address={"country": "CA"})
    print(f"{user}")
    assert user.frequent_shopper is True
    assert user.address.country=="CA"


def test_generate_user_with_factory():
    """Test that UserFactory generates a random user."""
    user: User = UserFactory(address__country="Canada")
    print(f"{user}")
    assert user.personal_info.first_name
    assert user.address.country == "Canada"
