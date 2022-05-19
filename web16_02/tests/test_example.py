import unittest
from src.example.ops import mul, sub, div, add


class TestExample(unittest.TestCase):
    """ Test math operation """

    @classmethod
    def setUpClass(cls) -> None:
        """Set Up Class"""
        print('Start all test')
        print('--------------')

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear Down Class"""
        print('End all test')
        print('--------------')

    def setUp(self):
        """Set Up for each test"""
        print(f'start test {self.shortDescription()}')

    def tearDown(self):
        """Tear Down for each test"""
        print(f'end test {self.shortDescription()}')

    def test_add(self):
        """ Add operation test """
        self.assertEqual(add(1, 2), 3)

    def test_sub(self):
        """ Sub operation test """
        self.assertEqual(sub(1, 2), -1)

    def test_mul(self):
        """ Mul operation test """
        self.assertEqual(mul(1, 2), 2)

    @unittest.skip('Так заманулося')
    def test_div(self):
        """ Div operation test """
        self.assertAlmostEqual(div(1, 3), 0.3333333)
