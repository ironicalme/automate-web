from typing import Sized

from hamcrest import empty, is_not


class IsNotEmpty:

    @classmethod
    def matches(cls, obj: Sized) -> bool:
        return is_not(empty()).matches(obj)
