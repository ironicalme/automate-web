from typing import Sized

from hamcrest import empty
from hamcrest import is_not


class IsNotEmpty:

    @classmethod
    def matches(cls, obj: Sized) -> bool:
        return is_not(empty()).matches(obj)
