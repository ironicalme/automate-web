from typing import Any

from hamcrest import equal_to


class IsEqualTo:

    def __init__(self, value: Any):
        self.value = value

    def matches(self, obj: Any) -> bool:
        return equal_to(self.value).matches(obj)
