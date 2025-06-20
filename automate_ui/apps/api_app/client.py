from urllib.parse import urljoin

from automate_ui.screenplay.core.api.rest_client import RestClient


class APIClient(RestClient):

    def __init__(self, base_url):
        super().__init__(base_url=urljoin(base_url, "/api/public/"))
        self.add_headers({"secret-header": "true"})  # bypass API rate limit

    def authenticate(self, api_key: str):
        self.add_headers({"Authorization": f"Api-Key {api_key}"})
        return self
