from dataclasses import dataclass
from typing import Optional, Tuple, Union
from certn_qa_tests.screenplay.abilities.use_phone import UsePhone
from certn_qa_tests.screenplay.actor import Actor
from certn_qa_tests.screenplay.mobile.target import Target
from appium.webdriver.webelement import WebElement


@dataclass
class ElementBoundaries:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Viewport:
    width: int
    height: int


class Scroll:
    """
    Scroll gesture on a mobile device.

    Usage:
        # Scrolling Element to Element

        Scroll().from_element(start_element).to_element(end_element).speed(1000)

        # Scrolling based off given coordinates

        Scroll().from_coords(start_x,start_y).to_coords(end_x, end_y)

        # Scrolling within the boundries of an element

        Scroll().left().within(an_element)

        # Scrolling in the viewport

        Scroll().down()

        # Scrolling in a direction from/to element

        Scroll().down().from_element(start_element)

        # Flick

        Scroll().up().flick().from_element(start_element)

        # Precise scrolling using steps. Usually used in wheel for iphone.

        Scroll().down().from_element(year_wheel_picker).steps(3)

    Use Scroll and `.with_speed()` in miliseconds to immitate swipe, and flick actions

    """

    def __init__(self):
        self.direction = None
        self.speed: int = 1000
        self.start_element: Target = None
        self.end_element: Target = None
        self.start_coords: Optional[Tuple[int, int]] = None
        self.end_coords: Optional[Tuple[int, int]] = None
        self.target_element: Target = None
        self.is_flick: bool = False
        self.steps: int = 1

    def up(self) -> "Scroll":
        """Set the scroll direction to up."""
        self.direction = "up"
        return self

    def down(self) -> "Scroll":
        """Set the scroll direction to down."""
        self.direction = "down"
        return self

    def left(self) -> "Scroll":
        """Set the scroll direction to left."""
        self.direction = "left"
        return self

    def right(self) -> "Scroll":
        """Set the scroll direction to right."""
        self.direction = "right"
        return self

    def with_speed(self, speed: int) -> "Scroll":
        """Speed at which to scroll in miliseconds"""
        self.speed = speed
        return self

    def from_element(self, element) -> "Scroll":
        self.start_element = element
        return self

    def to_element(self, element) -> "Scroll":
        self.end_element = element
        return self

    def from_coords(self, x, y) -> "Scroll":
        self.start_coords = (x, y)
        return self

    def to_coords(self, x, y) -> "Scroll":
        self.end_coords = (x, y)
        return self

    def flick(self) -> "Scroll":
        """Enable flick gesture."""
        self.is_flick = True
        return self

    def within(self, target: Target) -> "Scroll":
        """Scroll within the boundaries of a specific element."""
        self.target_element = target
        return self

    def step(self, steps: int) -> "Scroll":
        """Set the number of steps to scroll."""
        self.steps = steps
        return self

    def _get_driver(self, actor: Actor):
        return actor.get_ability(UsePhone).driver

    def _get_viewport(self, actor: Actor) -> Viewport:
        driver = self._get_driver(actor)
        viewport = driver.get_window_size()
        return Viewport(width=viewport["width"], height=viewport["height"])

    def _calculate_element_boundaries(self, element: WebElement) -> ElementBoundaries:
        """Calculate the boundaries of an element."""
        location = element.location
        size = element.size
        return ElementBoundaries(
            x=location['x'],
            y=location['y'],
            width=size['width'],
            height=size['height']
        )

    def _constrain_within_boundaries(self, x: int, y: int, boundaries: ElementBoundaries) -> Tuple[int, int]:
        """Constrain a coordinate to be within given boundaries."""
        x_max = boundaries.x + boundaries.width
        y_max = boundaries.y + boundaries.height
        constrained_x = max(boundaries.x, min(x, x_max - 1))
        constrained_y = max(boundaries.y, min(y, y_max - 1))
        return constrained_x, constrained_y

    def _calculate_element_center(self, element: WebElement) -> Tuple[int, int]:
        """Calculate the center of an element."""
        location = element.location
        size = element.size
        return location['x'] + size['width'] // 2, location['y'] + size['height'] // 2

    def _calculate_start_viewport_coordinates(self, viewport: Viewport, direction) -> Tuple[int, int]:
        """Calculate start coordinates for viewport-based scrolling."""
        # The gesture heuristic for viewport based scrolling was determined by ensuring the header, footer or sliding trays of MyCertn app lie within 20% off the edges.
        width = viewport.width
        height = viewport.height
        if direction in ["up", "down"]:
            return width // 2, int(height * (0.8 if direction == "up" else 0.2))  # Ensure it leaves 20% off the top and bottom edge
        elif direction in ["left", "right"]:
            return int(width * (0.8 if direction == "left" else 0.2)), height // 2  # Ensure it leaves 20% off the left and right edge
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def _calculate_end_viewport_coordinates(self, viewport: Viewport, direction, start_x, start_y) -> Tuple[int, int]:
        """Calculate end coordinates for viewport-based scrolling, constrained within viewport bounds."""
        width = viewport.width
        height = viewport.height
        if direction == "up":
            end_x = start_x
            end_y = max(0, start_y - int(height * 0.6))  # Ensure it doesn't go above the top of the viewport
        elif direction == "down":
            end_x = start_x
            end_y = min(height - 1, start_y + int(height * 0.6))  # Ensure it doesn't go below the bottom of the viewport
        elif direction == "left":
            end_x = max(0, start_x - int(width * 0.6))  # Ensure it doesn't go beyond the left edge
            end_y = start_y
        elif direction == "right":
            end_x = min(width - 1, start_x + int(width * 0.6))  # Ensure it doesn't go beyond the right edge
            end_y = start_y
        else:
            raise ValueError(f"Invalid direction: {direction}")
        return end_x, end_y

    def _calculate_end_coordinates_for_steps(
        self,
        viewport_or_boundaries: Union[Viewport, ElementBoundaries],
        direction: str,
        start_x: int,
        start_y: int,
        step: int,
    ) -> Tuple[int, int]:
        """
        Calculate end coordinates based on the number of steps,
        considering either viewport size or element boundaries.

        Args:
            viewport_or_boundaries: Can be a viewport size (dict) or element boundaries (ElementBoundaries).
            direction: Direction of the scroll ('up', 'down', 'left', 'right').
            start_x: Starting X coordinate.
            start_y: Starting Y coordinate.
            step: Number of steps to scroll

        Returns:
            Tuple[int, int]: Calculated end X and Y coordinates.
        """
        # Determine if we're working with viewport size or element boundaries
        # Why 20% of viewport hieight per step?
        # Predictable scrolling that does not skip a lot of visible elements.
        # Mimics real user's natural interaction
        # Balance between scrolling to little and too much.
        if isinstance(viewport_or_boundaries, Viewport):
            width = viewport_or_boundaries.width
            height = viewport_or_boundaries.height
            step_distance = int(height * 0.2)
            min_x, min_y, max_x, max_y = 0, 0, width - 1, height - 1
        # Why 12% of the element height per step?
        # Scrolls exactly 1 option on the picker wheel element
        # Optimum for other elements since they occupy a much smaller portion of the viewport.
        elif isinstance(viewport_or_boundaries, ElementBoundaries):
            min_x = viewport_or_boundaries.x
            min_y = viewport_or_boundaries.y
            max_x = viewport_or_boundaries.x + viewport_or_boundaries.width - 1
            max_y = viewport_or_boundaries.y + viewport_or_boundaries.height - 1
            step_distance = int(viewport_or_boundaries.height * 0.12)
        else:
            raise ValueError("Invalid viewport_or_boundaries type. Expected dict or ElementBoundaries.")

        # Calculate end coordinates based on the direction
        if direction == "up":
            end_x = start_x
            end_y = max(min_y, start_y - step_distance * step)  # Move up, constrained by min_y
        elif direction == "down":
            end_x = start_x
            end_y = min(max_y, start_y + step_distance * step)  # Move down, constrained by max_y
        elif direction == "left":
            end_x = max(min_x, start_x - step_distance * step)  # Move left, constrained by min_x
            end_y = start_y
        elif direction == "right":
            end_x = min(max_x, start_x + step_distance * step)  # Move right, constrained by max_x
            end_y = start_y
        else:
            raise ValueError(f"Invalid direction: {direction}")

        return end_x, end_y

    def _get_start_coordinates(self, actor) -> Tuple[int, int]:
        """Determine the start coordinates based on the provided element, coords or viewport."""

        if self.start_element:
            start_x, start_y = self._calculate_element_center(self.start_element.found_by(actor))
        elif self.start_coords:
            start_x, start_y = self.start_coords
        else:
            viewport = self._get_viewport(actor)
            start_x, start_y = self._calculate_start_viewport_coordinates(viewport, self.direction)

        if self.target_element:
            boundaries = self._calculate_element_boundaries(self.target_element.found_by(actor))
            start_x, start_y = self._constrain_within_boundaries(start_x, start_y, boundaries)

        return start_x, start_y

    def _get_end_coordinates(self, actor, start_x, start_y) -> Tuple[int, int]:
        """
        Determine the end coordinates based on the provided target element, coordinates, or viewport.

        Args:
            actor: The actor performing the action.
            start_x: The starting X coordinate.
            start_y: The starting Y coordinate.

        Returns:
            Tuple[int, int]: The calculated end X and Y coordinates.
        """

        if self.end_element:
            end_x, end_y = self._calculate_element_center(self.end_element.found_by(actor))
        elif self.end_coords:
            end_x, end_y = self.end_coords
        else:
            viewport = self._get_viewport(actor)

            if self.target_element:
                boundaries = self._calculate_element_boundaries(self.target_element.found_by(actor))
                if self.steps:
                    end_x, end_y = self._calculate_end_coordinates_for_steps(
                        boundaries, self.direction, start_x, start_y, self.steps
                    )
                else:
                    step_size = boundaries.height // 2 if self.direction in ("up", "down") else boundaries.width // 2
                    if self.direction == "up":
                        end_x = start_x
                        end_y = max(start_y - step_size, boundaries.y)  # Constrain to top boundary
                    elif self.direction == "down":
                        end_x = start_x
                        end_y = min(start_y + step_size, boundaries.y + boundaries.height - 1)  # Constrain to bottom
                    elif self.direction == "left":
                        end_x = max(start_x - step_size, boundaries.x)  # Constrain to left boundary
                        end_y = start_y
                    elif self.direction == "right":
                        end_x = min(start_x + step_size, boundaries.x + boundaries.width - 1)  # Constrain to right boundary
                        end_y = start_y
            else:
                if self.steps:
                    end_x, end_y = self._calculate_end_coordinates_for_steps(
                        viewport, self.direction, start_x, start_y, self.steps
                    )
                else:
                    end_x, end_y = self._calculate_end_viewport_coordinates(
                        viewport, self.direction, start_x, start_y
                    )

        return end_x, end_y

    def perform(self, actor: Actor):
        driver = self._get_driver(actor)

        # Calculate start and end coordinates
        start_x, start_y = self._get_start_coordinates(actor)
        end_x, end_y = self._get_end_coordinates(actor, start_x, start_y)

        duration = self.speed if not self.is_flick else max(1, self.speed // 2)

        # Perform the scroll action
        driver.swipe(start_x, start_y, end_x, end_y, duration=duration)
