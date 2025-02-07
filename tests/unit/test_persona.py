# import pytest
from automate_ui.screenplay.persona import User, get_user, UserFactory


def test_generate_random_user():
    """Test that get_user() generates a random user with default values."""
    user = get_user()
    assert user.personal_info.first_name
    assert user.address.country == "US"
    assert isinstance(user.frequent_shopper, bool)


def test_generate_user_with_specs():
    """Test that get_user() correctly overrides specified values."""
    user = get_user(frequent_shopper=True, address=UserFactory().address)
    assert user.frequent_shopper is True
    assert user.address


def test_generate_user_with_factory():
    """Test that UserFactory generates a random user."""
    user: User = UserFactory()
    assert user.personal_info.first_name
    assert user.address.country
