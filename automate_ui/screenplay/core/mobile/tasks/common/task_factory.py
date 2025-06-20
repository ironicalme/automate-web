from automate_ui.screenplay.core.mobile.tasks.common import BaseTask
from automate_ui.screenplay.core.mobile.tasks.common.task_registry import task_registry


class TaskFactory:

    @staticmethod
    def get_task(task_type: type[BaseTask], platform: str, **kwargs) -> BaseTask:
        key = f"{task_type.__name__}_{platform.lower()}"
        try:
            return task_registry.get(key, **kwargs)
        except KeyError as exc:
            raise ValueError(f"No Task registered with name {task_type.__name__} on platform: {platform}") from exc
