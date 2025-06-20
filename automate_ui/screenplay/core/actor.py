from __future__ import annotations
from typing import List, Type, Union, TypeVar, TYPE_CHECKING

from automate_ui.screenplay.core.narrator import Narrator
from .exceptions import UnableToPerformError
from .protocols import Forgettable, Performable, Describable

if TYPE_CHECKING:
    from .models.user.user import (
        User
    )

T_Ability = TypeVar("T_Ability", bound=Forgettable)
T_Persona = Union[
    "User",
    None]


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
