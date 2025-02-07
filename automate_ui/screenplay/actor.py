from __future__ import annotations
import copy
from typing import List, Type, Union, TypeVar, TYPE_CHECKING

from allure_commons._allure import StepContext

from automate_ui.screenplay.narrator import Narrator
from .exceptions import UnableToPerformError
from .protocols import Forgettable, Performable, Describable

if TYPE_CHECKING:
    from .persona import (
        User
    )

T_Ability = TypeVar("T_Ability", bound=Forgettable)
T_Persona = Union[
    "User",
    None]


def _generate_allure_params(task: Performable) -> dict:
    """
    Generates a dictionary of params to log in allure reports.
    Fetches all non-private/protected attributes from a task.
    Converts all values into JSON serializable format (strings).

    Note: This requires tasks to be responsible for implementing a __str__ method to support allure logging.
    Note: Only logs params for core screenplay tasks.
    """
    if "apps" in task.__module__:
        return {}
    params = copy.deepcopy(task.__dict__)
    json_serializable_params = {
        key: str(value)
        for key, value
        in params.items()
        if not key.startswith("_")
    }
    return json_serializable_params


class Actor:

    abilities: List[Forgettable]

    def __init__(self, name: str, narrator: Narrator = None) -> None:
        self._name = name
        self._persona = None
        self.abilities = []
        if not narrator:
            self.narrator = Narrator(name)
        self.narrate = self.narrator.logger.info

    def add_abilities(self, *abilities: T_Ability) -> "Actor":
        self.abilities.extend(abilities)
        return self

    def add_ability(self, ability: T_Ability) -> "Actor":
        self.abilities.append(ability)
        return self

    def get_ability(self, ability: Type[T_Ability]) -> T_Ability:
        for a in self.abilities:
            if isinstance(a, ability):
                return a
        raise UnableToPerformError(f"{self} does not have the Ability to {ability}")

    def has_ability(self, ability: Type[T_Ability]) -> bool:
        for a in self.abilities:
            if isinstance(a, ability):
                return True
        return False

    def attempts_to(self, *tasks: Performable) -> None:
        """
        Performs all tasks received in sequential order.
        Automatically outputs logs and generates allure test steps.
        """
        for task in tasks:
            if isinstance(task, Describable):
                self.narrate(f"{self.name} {task.describe()}")
            title = f"[{self.narrator.logger.name}] {str(type(task).__name__)}"
            with StepContext(title=title, params=_generate_allure_params(task)):
                task.perform(self)

    def cleanup(self) -> None:
        for ability in self.abilities:
            ability.forget()
        self.abilities = []

    @property
    def persona(self) -> T_Persona:
        return self._persona

    @persona.setter
    def persona(self, persona: T_Persona) -> None:
        self._persona = persona

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self.name
