"""Provide the test runner for catchlib."""

__all__: list[str] = ["test"]

import unittest


def test() -> unittest.TextTestResult:
    """Run all the tests."""
    loader: unittest.TestLoader
    suite: unittest.TestSuite
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="catchlib.tests")
    return unittest.TextTestRunner().run(suite)
