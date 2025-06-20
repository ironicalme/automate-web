from typing import Any

from hamcrest import is_


class IsTrue:

    @classmethod
    def matches(cls, obj: Any) -> bool:
        return is_(True).matches(obj)
