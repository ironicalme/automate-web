from abc import ABC, abstractmethod
from certn_qa_tests.screenplay.actor import Actor


class BaseTask(ABC):

    @abstractmethod
    def perform(self, actor: Actor):
        """Perform the task."""
