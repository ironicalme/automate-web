from abc import ABC, abstractmethod
from automate_ui.screenplay.core.actor import Actor


class BaseTask(ABC):

    @abstractmethod
    def perform(self, actor: Actor):
        """Perform the task."""
