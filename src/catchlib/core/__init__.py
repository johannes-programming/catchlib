from contextlib import contextmanager
from typing import *

__all__ = ["Catcher"]


class Catcher:

    "This class catches exceptions."

    __slots__ = ("_caught",)

    caught: Optional[BaseException]

    def __init__(self: Self) -> None:
        "This magic method initializes the current instance."
        self._caught = None

    @contextmanager
    def catch(self: Self, *args: type[BaseException]) -> Generator[Self, None, None]:
        "This contextmanager catches exceptions."
        self._caught = None
        exc: BaseException
        try:
            yield self
        except args as exc:
            self._caught = exc

    @property
    def caught(self: Self) -> Optional[BaseException]:
        "This property stores the caught exception."
        return self._caught
