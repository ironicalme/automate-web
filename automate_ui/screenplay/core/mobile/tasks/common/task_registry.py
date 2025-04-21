from typing import Literal, Union
from class_registry import ClassRegistry
from certn_qa_tests.screenplay.mobile.tasks.common import BaseTask

task_registry = ClassRegistry[BaseTask]()


def register_task(task_type, platform: Union[Literal["android"], Literal["ios"]]):
    """
    Decorator to register a task with the task_registry, using task_type and platform as keys.
    """
    def decorator(cls):
        # this key should be same as the key used to access the registry in TaskFactory
        key = f"{task_type.__name__}_{platform.lower()}"
        task_registry.register(key)(cls)
        return cls
    return decorator
