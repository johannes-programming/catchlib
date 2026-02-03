from contextlib import contextmanager
from typing import *

from overloadable import Overloadable

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
        exc: BaseException
        self._caught = None
        try:
            yield self
        except args as exc:
            self._caught = exc

    @property
    def caught(self: Self) -> Optional[BaseException]:
        "This property stores the caught exception."
        return self._caught

    @Overloadable
    def release(self: Self, *args: Any, **kwargs: Any) -> bool:
        "This method raises the caught exception."
        return bool(len(args) + len(kwargs))

    @release.overload(False)
    def release(self: Self) -> None:
        "This method raises the caught exception."
        exc: BaseException
        exc = self.caught
        self._caught = None
        if exc is not None:
            raise exc

    @release.overload(True)
    def release(self: Self, cause: Optional[BaseException]) -> None:
        "This method raises the caught exception."
        exc: BaseException
        exc = self.caught
        self._caught = None
        if exc is not None:
            raise exc from cause
