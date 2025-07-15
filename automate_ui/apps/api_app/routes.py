from dataclasses import dataclass

from automate_ui.apps.common.api.routes import URL


@dataclass
class Create(URL):
    def __init__(self, base_url: str):
        super().__init__(base_url + "create/")


@dataclass
class Events(URL):
    def __init__(self):
        super().__init__("events/")


@dataclass
class Group(URL):
    def __init__(self, base_url: str):
        super().__init__(base_url + "group/")


@dataclass
class Groups(URL):
    def __init__(self):
        super().__init__("groups/")

    def create(self) -> Create:
        return Create(self._url)

    def group(self, group_id) -> Group:
        return Group(self._url, group_id)


@dataclass
class User(URL):
    def __init__(self, base_url: str, user_id: str):
        super().__init__(base_url + f"{user_id}/")


@dataclass
class Users(URL):
    def __init__(self):
        super().__init__("users/")

    def create(self) -> Create:
        return Create(self._url)

    def fetch_user(self, user_id) -> User:
        return User(self._url, user_id)


@dataclass
class AppAPI:
    users = Users
    events = Events
    groups = Groups
    create = Create
    user = User
