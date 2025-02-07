from typing import Any

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class Answerable(Protocol):
    """Questions are answerable"""

    def answered_by(self, actor: "Actor") -> Any:
        """Direct the actor to answer a question by making an observation"""


@runtime_checkable
class Describable(Protocol):
    """Classes that describe themselves are Describable"""

    def describe(self) -> str:
        """Describe the Describable in the present tense."""


@runtime_checkable
class Forgettable(Protocol):
    """Abilities are Forgettable"""

    def forget(self) -> None:
        """
        Forget this Ability by doing any necessary cleanup (quitting browsers,
        closing connections, etc.)
        """


@runtime_checkable
class Performable(Protocol):
    """Tasks that can be performed are Performable"""

    def perform(self, actor: "Actor") -> None:
        """
        Direct the Actor to perform this Action.

        Args:
            actor: the Actor who will perform this Action.
        """


@runtime_checkable
class Matchable(Protocol):
    """Matchers are Matchable"""

    def matches(self, obj) -> bool:
        ...
