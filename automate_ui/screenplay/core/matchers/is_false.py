from typing import Any

from hamcrest import is_


class IsFalse:

    @classmethod
    def matches(cls, obj: Any) -> bool:
        return is_(False).matches(obj)
