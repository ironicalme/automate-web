from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.enums.keyboard_key import KeyboardKey
from automate_ui.screenplay.tasks.press_key import PressKey

if TYPE_CHECKING:
    from automate_ui.screenplay.core.actor import Actor
    from typing_extensions import Self


class Scroll:
    """Scrolls the page in a specified direction and/or amount.

    This class provides a way to scroll the browser window using either pixel deltas
    or keyboard shortcuts (HOME/END). Scrolling "up" corresponds to a negative
    delta_y, "down" to a positive delta_y, "left" to a negative delta_x, and
    "right" to a positive delta_x.

    The class offers convenient factory methods (`down`, `up`, `left`, `right`,
    `to_the_bottom`, `to_the_top`) for common scrolling actions. These factory
    methods ensure correct sign conventions for the delta values.

    Note: While it's possible to create a `Scroll` instance directly with
    `delta_x` and `delta_y` values, combining horizontal and vertical scrolling
    in a single `Scroll` action using deltas is not recommended. Instead,
    perform separate `Scroll` actions for each direction. The directional
    classmethod factory methods help enforce this best practice.

    Examples:
        actor.attempts_to(Scroll(delta_x=-20, delta_y=1200))  # Scroll up and right
        actor.attempts_to(Scroll.down(150))  # Scroll down 150 pixels
        actor.attempts_to(Scroll.left(2000))  # Scroll left 2000 pixels
        actor.attempts_to(Scroll.to_the_bottom())  # Scroll to the bottom of the page
        actor.attempts_to(Scroll.to_the_top())  # Scroll to the top of the page
        # actor.attempts_to(Scroll.down(150).left(50))  # Incorrect: Combining deltas in one Scroll

    Args:
        delta_x: The number of pixels to scroll horizontally. Negative values
            scroll left, positive values scroll right. Defaults to 0.
        delta_y: The number of pixels to scroll vertically. Negative values
            scroll up, positive values scroll down. Defaults to 0.
        key: An optional `KeyboardKey` to simulate a key press for scrolling
            (e.g., `KeyboardKey.HOME` or `KeyboardKey.END`). If provided,
            `delta_x` and `delta_y` are ignored. Defaults to None.
    """
    def __init__(
        self,
        delta_x: int = 0,
        delta_y: int = 0,
        key: Optional[KeyboardKey] = None
    ) -> None:
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.key = key

    @classmethod
    def down(cls, delta_y: int) -> Self:
        if delta_y < 0:
            delta_y = -delta_y
        return cls(delta_y=delta_y)

    @classmethod
    def to_the_bottom(cls) -> Self:
        return cls(key=KeyboardKey.END)

    @classmethod
    def up(cls, delta_y: int) -> Self:
        if delta_y > 0:
            delta_y = -delta_y
        return cls(delta_y=delta_y)

    @classmethod
    def to_the_top(cls) -> Self:
        return cls(key=KeyboardKey.HOME)

    @classmethod
    def left(cls, delta_x: int) -> Self:
        if delta_x > 0:
            delta_x = -delta_x
        return cls(delta_x=delta_x)

    @classmethod
    def right(cls, delta_x: int) -> Self:
        if delta_x < 0:
            delta_x = -delta_x
        return cls(delta_x=delta_x)

    def describe(self) -> str:
        return f"scrolls the page {self.loggable_direction}."

    @property
    def loggable_direction(self) -> str:
        if self.key == KeyboardKey.HOME:
            return "to the top"

        if self.key == KeyboardKey.END:
            return "to the bottom"

        if not self.delta_x and not self.delta_y:
            return "nowhere"

        x_dir = y_dir = x_val = y_val = x_descr = y_descr = ''

        if self.delta_x:
            x_dir = 'right' if self.delta_x > 0 else 'left'
            x_val = abs(self.delta_x)
            x_descr = f"{x_val} pixels {x_dir}"

        if self.delta_y:
            y_dir = 'down' if self.delta_y > 0 else 'up'
            y_val = abs(self.delta_y)
            y_descr = f"{y_val} pixels {y_dir}"

        return f"{x_descr}{' and ' if x_val and y_val else ''}{y_descr}"

    def perform(self, actor: Actor = None) -> None:
        if self.key:
            actor.attempts_to(PressKey(self.key))
            return

        page = actor.get_ability(BrowseTheWeb).current_page
        page.mouse.wheel(delta_x=self.delta_x, delta_y=self.delta_y)
