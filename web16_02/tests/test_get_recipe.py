import unittest
from unittest.mock import mock_open, patch
from src.get_recipe.get_recipe import get_recipe


class TestGetRecipe(unittest.TestCase):
    mock_open_file = None

    def setUp(self):
        """Set Up for each test"""
        self.mock_open_file = mock_open(
            read_data='60b90c2413067a15887e1ae2,Lemon Pancakes,2 tablespoons baking powder,1 cup vanilla-flavored almond milk,1 lemon\n60b90c2e13067a15887e1ae3,Chicken and Cold Noodles,6 ounces dry Chinese noodles,1 tablespoon sesame oil,3 tablespoons soy sauce')

    def tearDown(self):
        """Tear Down for each test"""
        self.mock_open_file = None

    # @patch('builtins.open', mock_open_file)
    def test_get_first_recipe(self):
        """ Test get first recipe """
        s_id = '60b90c2413067a15887e1ae2'
        path = 'fake.csv'
        with patch('builtins.open', self.mock_open_file) as mock_open_file:
            result = get_recipe(path, s_id)
            self.assertEqual(s_id, result.get('id'))
            self.assertEqual('Lemon Pancakes', result.get('name'))

    # @patch('builtins.open', mock_open_file)
    def test_get_last_recipe(self):
        """ Test get first recipe """
        s_id = '60b90c2e13067a15887e1ae3'
        path = 'fake.csv'
        with patch('builtins.open', self.mock_open_file) as mock_open_file:
            result = get_recipe(path, s_id)
            mock_open_file.assert_called()  # ошибка будет если мок не вызвали
            assert 'r' in mock_open_file.call_args_list[0][0], 'Файл должен быть открыт только для чтения'
            self.assertEqual(s_id, result.get('id'))
