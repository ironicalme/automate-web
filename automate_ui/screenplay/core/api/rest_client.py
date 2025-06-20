import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type, TypeVar, Union
from urllib.parse import urljoin

import requests
from pydantic import BaseModel, ValidationError

from automate_ui.screenplay.core.exceptions import RestClientError

Model_T = TypeVar("Model_T", bound=BaseModel)


class RestClient(ABC):
    def __init__(self, base_url: Optional[str]):
        self._session = requests.Session()
        self._base_url = base_url
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

    @abstractmethod
    def authenticate(self, *args, **kwargs) -> None:
        pass

    def add_headers(self, headers: Dict[str, str]) -> None:
        self._session.headers.update(headers)

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def base_url(self) -> Union[str, None]:
        return self._base_url

    def construct_url(self, url: str) -> str:
        return urljoin(self._base_url, url)

    def validate_response(self, response: requests.Response) -> None:
        """
        Ensures that a response has a 200 OK status.
        If not, raises a RestClientError with details.
        """
        if not response.ok:
            try:
                error_body = response.json()
            except requests.exceptions.JSONDecodeError:
                error_body = response.text
            print(f"################{response.request.body}")
            raise RestClientError(response.status_code, response.url, error_body)

    def model_response(
        self,
        model: Type[Model_T],
        response: requests.Response,
        expect_list: bool = False,
    ) -> Union[Model_T, List[Model_T], bytes]:
        """
        Maps a response object to a specified Pydantic model.
        If expect_list is True or response is detected to be a list,
        returns a list of model instances.
        Otherwise, returns a single model instance.
        Returns raw bytes if JSON decoding fails.
        Logs ValidationErrors during parsing.
        """
        self.validate_response(response)

        try:
            json_data = response.json()
        except requests.exceptions.JSONDecodeError:
            self._logger.error(
                f"Failed to decode JSON from response: {response.content}"
            )
            return response.content

        is_list = expect_list or isinstance(json_data, list)

        try:
            if is_list:
                if not isinstance(json_data, list):
                    self._logger.error(
                        f"Expected list response but got: {type(json_data)}"
                    )
                    return response.content

                result = []
                for item in json_data:
                    result.append(model.model_validate(item))
                return result
            else:
                return model.model_validate(json_data)
        except ValidationError as ex:
            self._logger.error(
                f"Validation error when mapping response from {response.url} to '{model.__name__}':\n{ex}"
            )
            return response.content
