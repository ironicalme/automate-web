from typing import Any

from hamcrest import equal_to
from hamcrest import is_not


class IsNotEqualTo:

    def __init__(self, value: Any):
        self.value = value

    def matches(self, obj: Any) -> bool:
        return is_not(equal_to(self.value)).matches(obj)
