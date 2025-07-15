from abc import ABC
from abc import abstractmethod

from automate_ui.screenplay.core.actor import Actor


class BaseTask(ABC):

    @abstractmethod
    def perform(self, actor: Actor):
        """Perform the task."""
