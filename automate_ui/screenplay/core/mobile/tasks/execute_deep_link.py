from certn_qa_tests.screenplay.abilities.use_phone import UsePhone
from certn_qa_tests.screenplay.actor import Actor
from certn_qa_tests.screenplay.mobile.tasks.common import (
    BaseTask,
    register_task,
    TaskPerformer
)


class ExecuteDeepLink(TaskPerformer):
    def __init__(self, deep_link_url: str, package_name: str = None) -> None:
        super().__init__(ExecuteDeepLink, deep_link_url=deep_link_url, package_name=package_name)


@register_task(ExecuteDeepLink, "android")
class AndroidExecuteDeepLink(BaseTask):
    def __init__(self, deep_link_url: str, package_name: str) -> None:
        self.deep_link_url = deep_link_url
        self.package_name = package_name

    @classmethod
    def describe(cls) -> str:
        return "switches MyCertn app to development environment"

    def perform(self, actor: Actor):
        driver = actor.get_ability(UsePhone).driver
        driver.execute_script("mobile: deepLink", {
            "url": self.deep_link_url,
            "package": self.package_name
        })


@register_task(ExecuteDeepLink, "ios")
class IosExecuteDeepLink(BaseTask):
    def __init__(self, deep_link_url: str, package_name: str) -> None:
        self.deep_link_url = deep_link_url
        self.package_name = package_name

    @classmethod
    def describe(cls) -> str:
        return "switches MyCertn app to development environment"

    def perform(self, actor: Actor):
        driver = actor.get_ability(UsePhone).driver
        driver.execute_script("mobile: deepLink", {
            "url": self.deep_link_url,
            "bundleId": self.package_name
        })
