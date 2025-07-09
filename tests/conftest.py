from pathlib import Path
from typing import Optional, Union
import pytest

from selenium.common.exceptions import SessionNotCreatedException

from automate_ui.enums.timeouts import Timeouts
from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.abilities.use_phone import PhoneCapabilities, UsePhone
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.mobile.constants import PACKAGE_NAME
from automate_ui.screenplay.core.models.user.generate_user import GenerateUserPersona
from automate_ui.screenplay.core.models.user.user import User
from automate_ui.screenplay.core.ui.tasks.screenshot_page import ScreenshotPage
# from playwright._impl._api_structures import ViewportSize
from automate_ui.common.utils.config_manager import create_config_manager


def pytest_addoption(parser):
    """Add command-line options for configuration override."""
    parser.addoption(
        "--yaml-config",
        action="store",
        default="local_secrets.yaml",
        help="Path to YAML configuration file (default: local_secrets.yaml)"
    )
    parser.addoption(
        "--aws-secret",
        action="store",
        default=None,
        help="AWS Secrets Manager secret name to use instead of YAML"
    )
    parser.addoption(
        "--aws-region",
        action="store",
        default=None,
        help="AWS region for Secrets Manager (default: uses AWS default)"
    )
    parser.addoption(
        "--env",
        action="store",
        default="development",
        choices=["development", "staging", "production"],
        help="Environment to use for configuration (default: development)"
    )


@pytest.fixture(scope='session')
def config_manager(request):
    """
    Pytest fixture to provide a config manager that combines secrets with environment URLs.

    Usage:
        def test_something(config_manager):
            api_key = config_manager.get_secret('api.public.key')
            api_url = config_manager.get_url('api.public', 'base_url')
            web_url = config_manager.get_url('web_app', 'base_url')

    Command-line options:
        --yaml-config: Path to YAML file (default: local_secrets.yaml)
        --aws-secret: AWS Secrets Manager secret name
        --aws-region: AWS region for Secrets Manager
        --env: Environment to use (development/staging/production, default: development)
    """
    yaml_file_path = request.config.getoption("--yaml-config")
    aws_secret_name = request.config.getoption("--aws-secret")
    aws_region = request.config.getoption("--aws-region")
    environment = request.config.getoption("--env")

    return create_config_manager(
        yaml_file_path=yaml_file_path,
        environment=environment,
        aws_secret_name=aws_secret_name,
        aws_region=aws_region
    )





@pytest.fixture(scope='class')
def actor_factory():
    def generate_actor(
        name: str,
        abilities,
        persona: Optional[Union["User"]] = None,  # Add more Personas as required
        timeout: Optional[int] = 1000 * 60
    ) -> Actor:
        actor = Actor(name=name)
        actor.add_abilities(*abilities)
        actor.persona = persona
        if actor.has_ability(BrowseTheWeb):
            browse_the_web = actor.get_ability(BrowseTheWeb)
            page = browse_the_web.browser.new_page()
            # new_context = browse_the_web.browser.new_context(
            #     locale="en-US",
            #     # extra_http_headers={"bypass_rt": "true"},  # bypass API rate limit
            #     # screen=ViewportSize(width=1920, height=1080) # screensize freeze
            # )
            # page = new_context.new_page()
            page.set_default_timeout(timeout=timeout)
            browse_the_web.current_page = page
            browse_the_web.pages.append(page)
        return actor
    return generate_actor


@pytest.fixture
def frequent_shopper(
    playwright,
    actor_factory,
    take_screenshot_on_test_failure
) -> Actor:
    persona = GenerateUserPersona() \
        .with_personal_info(phone_country="Canada") \
        .with_address(country="Canada") \
        .with_personal_info() \
        .with_email() \
        .with_password() \
        .build()

    user = actor_factory(
        name=persona.personal_information.name.given_name,
        abilities=(
            BrowseTheWeb.using_chromium(playwright),
            # Add more abilities as requred
        ),
        persona=persona
    )

    yield user

    take_screenshot_on_test_failure(user)

    user.cleanup()


@pytest.fixture
def take_screenshot_on_test_failure(request):
    def take_screenshot(actor: Actor):

        actor_involved_in_failed_test = request.node.rep_setup.failed or request.node.rep_call.failed

        if actor_involved_in_failed_test:
            partial_path = f"{request.node.name}/{actor.name.replace(' ', '-').lower()}/screenshot.png"
            actor.attempts_to(ScreenshotPage.saved_as(file_name=partial_path, file_type="png"))
    return take_screenshot


# Mobile

@pytest.fixture
def android_phone_capabilities() -> PhoneCapabilities:
    phone_capabilities = PhoneCapabilities(
        platform_name='Android',
        automation_name='uiautomator2',
        device_name='Medium_Phone_API_35',
        language='en',
        locale='US',
        session_timeout=Timeouts.APPIUM_SESSION_TIMEOUT,
    )
    return phone_capabilities


@pytest.fixture
def ios_phone_capabilities() -> PhoneCapabilities:
    phone_capabilities = PhoneCapabilities(
        platform_name='iOS',
        automation_name='XCUITest',
        device_name='iPhone 15 Pro Max',
        platform_version='18.1',
        no_reset=False,
        session_timeout=Timeouts.APPIUM_SESSION_TIMEOUT,
    )
    return phone_capabilities


@pytest.fixture
def create_actor_with_phone(
    appium_server_url,
):
    def _create_actor(
        name: str,
        phone_capabilities,  # This is the object, not a dictionary
        persona: Optional["User"] = None,
    ) -> Actor:
        actor = Actor(name=name)

        use_phone_instance = UsePhone.with_capabilities(phone_capabilities)
        actor.add_ability(use_phone_instance)

        actor.persona = persona

        if actor.has_ability(UsePhone):
            use_phone_ability = actor.get_ability(UsePhone)
            try:
                use_phone_ability.start_session(appium_server_url)
                driver = use_phone_ability.driver
                platform = driver.capabilities.get("platformName").lower()
                package_name = PACKAGE_NAME  # this is bundle ID for ios.

                if driver.is_app_installed(package_name):
                    driver.remove_app(package_name)

                app_path = Path("resources/MyApp.apk" if platform == "android" else "resources/MyApp.app")
                if not Path.exists(app_path):
                    raise FileNotFoundError(
                        f"The app installable (.apk/.ipa) was not found at path: {app_path}."
                    )
                # An iOS simulator requires a simulator build, that is a directory.
                if platform == "ios" and app_path.is_dir():
                    driver.install_app(str(app_path))
                elif platform == "android":
                    driver.install_app(str(app_path))
                else:
                    raise RuntimeError(f"Cannot install the app with the installable provided at path: {app_path}")

                driver.activate_app(package_name)

            except SessionNotCreatedException as e:
                raise RuntimeError(f"Failed to start the Appium session: {e}") from e

        return actor

    return _create_actor


@pytest.fixture
def android_actor_factory(
    create_actor_with_phone,
    android_phone_capabilities
):
    def generate_android_actor(
        name: str,
        persona: Optional["User"] = None,
    ) -> Actor:
        return create_actor_with_phone(
            name=name,
            phone_capabilities=android_phone_capabilities,
            persona=persona
        )
    return generate_android_actor


@pytest.fixture
def ios_actor_factory(
    create_actor_with_phone,
    ios_phone_capabilities
):
    def generate_ios_actor(
        name: str,
        persona: Optional["User"] = None,
    ) -> Actor:
        return create_actor_with_phone(
            name=name,
            phone_capabilities=ios_phone_capabilities,
            persona=persona
        )
    return generate_ios_actor