from typing import Any, Callable

import wrapt
from deepdiff import DeepDiff

from automate_ui.screenplay.abilities.browse_the_web import BrowseTheWeb
from automate_ui.screenplay.core.actor import Actor


def diffs(left, right):
    excluded_paths = getattr(left, "exclude_paths", [])
    if "exclude_paths" not in excluded_paths:
        excluded_paths.append("exclude_paths")
    return DeepDiff(left, right, verbose_level=2, exclude_paths=excluded_paths)


def is_equal(left, right):
    """
    The resulting overridden __eq__ method in dataclasses decorated by @deep_diffs
    """
    if diffs(left, right):
        return False
    return True


def pytest_friendly_eq_summary(left, right) -> list[str]:
    """
    Provides a custom pytest assert message for @deep_diffs decorated dataclasses.
    Used in conftest in the 'pytest_assertrepr_compare' hook.
    """
    # Provide name of classes being compared
    final_output = [f"{left.__class__.__name__} == {right.__class__.__name__}"]

    if not isinstance(left, type(right)):
        final_output.append("objects are different types")
        return final_output

    raw_diffs = diffs(left, right)

    # Provide human readable sentences of differences
    pretty_msg = raw_diffs.pretty()
    pretty_msgs = [
        sentence.rjust(len(sentence) + 4).replace("root.", "")
        for sentence in pretty_msg.split("\n")
    ]
    final_output.append(f"{len(pretty_msgs)} change(s) detected")
    final_output.append("Summary:")
    final_output.extend(pretty_msgs)

    # Provide excluded paths
    excluded_paths = getattr(left, "exclude_paths", [])
    if excluded_paths:
        excluded_paths = [f"    {path}" for path in excluded_paths]
        final_output.append("Paths excluded from comparison:")
        final_output.extend(excluded_paths)

    return final_output


@wrapt.decorator
def deep_diffs(wrapped, instance=None, args=None, kwargs=None):
    """
    Can be decorated to dataclasses providing enhanced equality checking and logging.
    Paths can be ignored by providing the decorated dataclass an `exclude_paths: list[str]` attribute.
    """
    wrapped.__eq__ = is_equal
    return wrapped(*args, **kwargs)


def indent_logs(func: Callable[[Any, Actor], Any]):
    """
    Can be used to indent the logs produced by a decorated method.
    Useful for improving readability and breaking down high-level tasks into heading/content-like structures.
    Primarily intended for Tasks & Questions.

    Requires:
        Actor (taken from the decorated method).
    """

    def wrapper(*args, **kwargs) -> None:
        actor = None

        for arg in args:
            if isinstance(arg, Actor):
                actor = arg

        if not actor:
            raise Exception("No actor was provided to decorated Callable")

        actor.narrator.add_indent()
        func(*args, **kwargs)
        actor.narrator.remove_indent()

    return wrapper


def expect_navigation(timeout=15):
    """
    Wraps a Task's perform method with the playwright expect_navigation() method

    Requires:
        Actor (taken from the decorated method).
        BrowseTheWeb (Ability)
    """

    def _expect_navigation(func: Callable[[Any, Actor], Any]):
        def wrapper(*args, **kwargs) -> None:
            actor = None

            for arg in args:
                if isinstance(arg, Actor):
                    actor = arg

            if not actor:
                raise Exception("No actor was provided to decorated Callable")

            page = actor.get_ability(BrowseTheWeb).current_page
            with page.expect_navigation(timeout=timeout * 1000):
                func(*args, **kwargs)

        return wrapper

    return _expect_navigation
