from __future__ import annotations
from automate_ui.screenplay.actor import Actor
from automate_ui.screenplay.protocols import Answerable, Performable, Matchable
import waiter
from automate_ui.screenplay.exceptions import WaitTimeoutError, UnableToActError


class Wait:

    def __init__(self) -> None:
        """
        Waits until a question returns the specified answer.
        Timeout and polling frequency adjustable, by default checks every 3 seconds for 15 seconds.
        Raises a WaitTimeoutError exception if a timeout occurs.
        """
        self._question = None
        self._poll = None
        self._timeout = None
        self._loggable_question = None
        self._appended_task = None
        self._matcher = None

    def until(self, question: Answerable, matcher: Matchable):
        self._question = question
        self._matcher = matcher
        return self

    @property
    def loggable_question(self):
        try:
            question_name = self._question.__name__
        except AttributeError:
            question_name = self._question.__class__.__name__
        return question_name

    @property
    def loggable_condition(self):
        try:
            condition_name = self._matcher.__name__
        except AttributeError:
            condition_name = self._matcher.__class__.__name__
        return condition_name

    def for_(self, seconds: int):
        """
        Set for how long the actor should continue trying.
        """
        self._timeout = seconds
        return self

    trying_for_no_longer_than = trying_for = waiting_for = for_

    def polling(self, seconds: int):
        """
        Adjust the polling frequency.
        """
        self._poll = seconds
        return self

    polling_every = trying_every = polling

    def after_failed_attempt(self, task: Performable):
        """
        Optionally directs the actor to perform a task in-between polling attempts, such as refreshing the page.
        """
        self._appended_task = task
        return self

    def perform(self, actor: Actor) -> None:
        if not self._question or self._matcher is None:
            raise UnableToActError("both an Answerable and Resolvable is required to perform this action.")

        if not self._poll:
            self._poll = 3

        if not self._timeout:
            self._timeout = 15

        if self._poll > self._timeout:
            raise UnableToActError("Polling period must be less than or equal to timeout")

        for _ in waiter.wait(self._poll, self._timeout):
            answer = self._question.answered_by(actor)
            if self._matcher.matches(answer):
                return
            if self._appended_task:
                actor.attempts_to(self._appended_task)

        raise WaitTimeoutError(
            f"Timed out waiting for: '{self.loggable_question}' to match condition: '{self.loggable_condition}'"
        )
