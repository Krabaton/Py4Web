import unittest
from unittest.mock import patch
from src.method.main import ttt
import json


class TestClass(unittest.TestCase):
    """ Test our class """

    @patch('json.dump')
    def test_ttt(self, dump_mock):
        """ Test json dumps """
        ttt()
        dump_mock.assert_called()
