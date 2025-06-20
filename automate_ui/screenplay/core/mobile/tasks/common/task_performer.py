from typing import Type
from automate_ui.screenplay.core.actor import Actor
from automate_ui.screenplay.core.decorators import indent_logs
from .base_task import BaseTask
from automate_ui.screenplay.abilities import UsePhone
from .task_factory import TaskFactory


class TaskPerformer:
    def __init__(self, task_type: Type[BaseTask], **task_args) -> None:
        self.task_type = task_type
        self.task_args = task_args

    @indent_logs
    def perform(self, actor: Actor) -> None:
        platform = actor.get_ability(UsePhone).capabilities.get("platformName")
        platform_task = TaskFactory.get_task(
            self.task_type, platform, **self.task_args
        )
        actor.attempts_to(platform_task)
