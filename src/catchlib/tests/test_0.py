import unittest
from typing import *

from catchlib.core import Catcher


class TestCatcher(unittest.TestCase):
    def test_captures_matching_exception(self: Self) -> None:
        catcher: Catcher = Catcher()
        with catcher.catch(ValueError):
            raise ValueError("bad value")
        self.assertIsNotNone(catcher.caught)
        self.assertIsInstance(catcher.caught, ValueError)
        self.assertEqual(str(catcher.caught), "bad value")

    def test_no_exception_leaves_caught_none(self: Self) -> None:
        catcher: Catcher = Catcher()
        with catcher.catch(ValueError):
            pass
        self.assertIsNone(catcher.caught)

    def test_captures_one_of_multiple_types(self: Self) -> None:
        catcher: Catcher = Catcher()
        with catcher.catch(ValueError, KeyError):
            raise KeyError("missing")
        self.assertIsNotNone(catcher.caught)
        self.assertIsInstance(catcher.caught, KeyError)
        self.assertEqual(
            str(catcher.caught), "'missing'"
        )  # KeyError stringifies with quotes

    def test_non_matching_exception_propagates_and_does_not_set_caught(
        self: Self,
    ) -> None:
        catcher: Catcher = Catcher()
        with self.assertRaises(ZeroDivisionError):
            with catcher.catch(ValueError, KeyError):
                1 / 0  # ZeroDivisionError not in capture set
        # Since the exception propagated out, Catcher should not have recorded anything
        self.assertIsNone(catcher.caught)

    def test_reuse_and_reset_semantics(self: Self) -> None:
        catcher: Catcher = Catcher()

        # First, capture an exception
        with catcher.catch(RuntimeError):
            raise RuntimeError("first")
        self.assertIsInstance(catcher.caught, RuntimeError)

        # Next, a clean block should reset caught to None
        with catcher.catch(RuntimeError):
            pass
        self.assertIsNone(catcher.caught)

        # Finally, capture another (different) exception type by passing multiple
        with catcher.catch(RuntimeError, TypeError):
            raise TypeError("second")
        self.assertIsInstance(catcher.caught, TypeError)

    def test_empty_type_tuple_never_catches(self: Self) -> None:
        catcher: Catcher = Catcher()
        # Passing no types should behave like catching nothing: exception propagates
        with self.assertRaises(ValueError):
            with catcher.catch():
                raise ValueError("won't be caught")
        self.assertIsNone(catcher.caught)


if __name__ == "__main__":
    unittest.main()
