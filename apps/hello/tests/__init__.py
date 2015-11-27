import unittest


def suite():
    return unittest.TestLoader().discover("hello.tests", pattern="*.py")
