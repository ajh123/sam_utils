import unittest
from test_main import TestValidatedInput, TestValidatedListInput
from test_maths import TestIsEven, TestIsNumeric, TestIsPositive

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestValidatedInput())
    suite.addTest(TestValidatedListInput())
    suite.addTest(TestIsEven())
    suite.addTest(TestIsNumeric())
    suite.addTest(TestIsPositive())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())