import requests

from automate_ui.screenplay.abilities.send_http_requests import SendHttpRequests
from automate_ui.screenplay.core.actor import Actor


class Response:

    def __init__(self, name: str = None, latest: bool = None):
        self.name = name
        self.latest = latest

    @classmethod
    def of_request_named(cls, name: str) -> "Response":
        return Response(name=name)

    @classmethod
    def of_latest_request(cls) -> "Response":
        return Response(latest=True)

    def sent_by(self, actor: Actor) -> requests.Response:
        if not self.name and not self.latest:
            raise Exception("No criteria was provided to filter responses")

        saved_responses = actor.get_ability(SendHttpRequests).responses

        if not saved_responses:
            raise Exception(
                "Unable to fetch a response as the responses list is currently empty."
            )

        if self.latest:
            _, response = saved_responses[-1]
            return response

        matched_responses = [response for self.name, response in saved_responses]

        if not matched_responses:
            raise Exception(f"No response matching name: '{self.name}' was found")

        if len(matched_responses) > 1:
            actor.narrator.logger.warning(
                f"Multiple responses were found matching name: {self.name}, returning latest"
            )
        return matched_responses[-1]
