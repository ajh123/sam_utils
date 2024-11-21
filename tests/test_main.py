import unittest
from unittest import mock
from sam_utilities.main import *

class TestValidatedInput(unittest.TestCase):
    @mock.patch('sam_utilities.main.input', create=True)
    def runTest(self, mocked_input):
        # Simulate invalid input followed by valid input
        mocked_input.side_effect = ["bob", "ddfdsfdsdf", "fdfdggfdfdggf", 42]
        
        # Call the function with int type
        res = validated_input(int, "Input a number")
        
        # Check if the result is of type int and equals 42
        self.assertEqual(res, 42)
        self.assertEqual(type(res), int)

class TestValidatedListInput(unittest.TestCase):
    @mock.patch('sam_utilities.main.input', create=True)
    def runTest(self, mocked_input):
        # Simulate invalid input followed by valid input
        data = ["bob", "chicken", "house"]
        mocked_input.side_effect = ["bob", "ddfdsfdsdf", "fdfdggfdfdggf", 42, "house"]
        
        # Call the function with int type
        res = validate_list_input(data, "Input list member")
        
        # Check if the result is in the list
        self.assertIn(res, data)
