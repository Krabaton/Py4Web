import unittest
from unittest.mock import patch
from src.reduce_sum.answer import numbers, sum_numbers
import src.reduce_sum.answer


class TestClass(unittest.TestCase):
    """ Test reduce method """

    def test_result(self):
        """ test result function sum_numbers """
        result = sum_numbers(numbers)
        self.assertEqual(result, 96)

    @patch('src.reduce_sum.answer.other')
    def test_other(self, mock_other):
        """ test result function sum_numbers without other"""
        result = sum_numbers(numbers)
        self.assertEqual(result, 96)
        mock_other.assert_called()

    @patch('src.reduce_sum.answer.other')
    def test_reduce(self, mock_other):
        """ Test reduce """
        with patch.object(src.reduce_sum.answer, 'reduce', create=True) as r_mock:
            r_mock.return_value = 96
            result = sum_numbers(numbers)
            self.assertEqual(result, 96)
            r_mock.assert_called()
