import unittest
from sam_utilities.maths import *

class TestIsEven(unittest.TestCase):
    def runTest(self):
        res = is_even(2)
        self.assertEqual(res, True)
        res = is_even(1)
        self.assertEqual(res, False)
        res = is_even(2.4)
        self.assertEqual(res, False)

class TestIsNumeric(unittest.TestCase):
    def runTest(self):
        res = is_numeric(2)
        self.assertEqual(res, True)
        res = is_numeric(1)
        self.assertEqual(res, True)
        res = is_numeric("bob")
        self.assertEqual(res, False)

class TestIsPositive(unittest.TestCase):
    def runTest(self):
        res = is_positive(2)
        self.assertEqual(res, True)
        res = is_positive(1)
        self.assertEqual(res, True)
        res = is_positive("bob")
        self.assertEqual(res, False)
        res = is_positive(-1)
        self.assertEqual(res, False)