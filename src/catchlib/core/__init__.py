from contextlib import contextmanager
from typing import *

__all__ = ["Catcher"]

DEFAULT = object()


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

    @overload
    def release(self: Self) -> None: ...

    @overload
    def release(self: Self, cause: Optional[BaseException]) -> None: ...

    def release(
        self: Self,
        cause: BaseException | None | object = DEFAULT,
    ) -> None:
        "This method raises the caught exception."
        exc: BaseException
        exc = self.caught
        self._caught = None
        if exc is None:
            return
        if cause is DEFAULT:
            raise exc
        else:
            raise exc from cause
