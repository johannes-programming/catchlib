"""This module defines the Catcher class."""

from __future__ import annotations

__all__: list[str] = ["Catcher"]

import enum
from collections.abc import Generator
from contextlib import contextmanager
from typing import Optional, Self, overload


class Missing(enum.Enum):
    """Sentinel to detect missing cause argument."""

    missing = None


class Catcher:
    """Catch exceptions."""

    __slots__ = ("_caught",)

    _caught: Optional[BaseException]

    def __init__(self: Self) -> None:
        """Initialize the catcher."""
        self._caught = None

    @contextmanager
    def catch(
        self: Self, *args: type[BaseException]
    ) -> Generator[Self, None, None]:
        """Catch exceptions of the given types."""
        exc: BaseException
        self._caught = None
        try:
            yield self
        except args as exc:
            self._caught = exc

    @property
    def caught(self: Self) -> Optional[BaseException]:
        """Return the caught exception."""
        return self._caught

    @overload
    def release(self: Self) -> None: ...

    @overload
    def release(self: Self, cause: Optional[BaseException]) -> None: ...

    def release(
        self: Self,
        cause: Optional[BaseException] | Missing = Missing.missing,
    ) -> None:
        """Raise and clear the caught exception."""
        exc: Optional[BaseException]
        exc = self.caught
        self._caught = None
        if exc is None:
            return
        if isinstance(cause, Missing):
            raise exc
        else:
            raise exc from cause
