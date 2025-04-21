import json
from typing import Optional
from pydantic import BaseModel, Field
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios.xcuitest.base import XCUITestOptions


class PhoneCapabilities(BaseModel):
    platform_name: str = Field(serialization_alias="platformName")
    automation_name: str = Field(serialization_alias="automationName")
    device_name: str = Field(serialization_alias="deviceName")
    # app_package and app_activity are now being set in create_actor_with_phone() fixture
    app_package: str = Field(default=None, serialization_alias="appPackage")
    app_activity: str = Field(default=None, serialization_alias="appActivity")
    platform_version: str = Field(default=None, serialization_alias="platformVersion")
    session_timeout: int = Field(default=None, serialization_alias="newCommandTimeout")
    udid: str = Field(default=False, serialization_alias="udid")
    no_reset: bool = Field(default=False, serialization_alias="noReset")
    # below ones are optional for iOS
    language: Optional[str] = None
    locale: Optional[str] = None


class UsePhone:
    def __init__(self, capabilities: PhoneCapabilities) -> None:
        json_capabilities = capabilities.model_dump_json(by_alias=True)
        self.capabilities: dict = json.loads(json_capabilities)
        self.driver = None

    @staticmethod
    def with_capabilities(capabilities: PhoneCapabilities) -> "UsePhone":
        return UsePhone(capabilities)

    def start_session(self, appium_server_url: str):
        platform = self.capabilities.get('platformName', '').lower()

        if platform == "android":
            options = UiAutomator2Options().load_capabilities(self.capabilities)
        elif platform == "ios":
            options = XCUITestOptions().load_capabilities(self.capabilities)
        else:
            raise ValueError(f"Unsupported platform: {self.capabilities.get('platformName')}")

        self.driver = webdriver.Remote(command_executor=appium_server_url, options=options)

    def forget(self) -> None:

        if self.driver:
            self.driver.quit()

    def __repr__(self) -> str:
        return self.__class__.__name__
