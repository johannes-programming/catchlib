import unittest

__all__ = ["test"]


def test() -> unittest.TextTestRunner:
    "This function runs all the tests."
    loader: unittest.TestLoader
    tests: unittest.TestSuite
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="catchlib.tests")
    return unittest.TextTestRunner().run(tests)
