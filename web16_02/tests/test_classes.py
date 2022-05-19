import unittest
from src.my_class.main import Cat, Dog, CatDog, DogCat, Animal


class TestClass(unittest.TestCase):
    """ Test our class """

    def test_dog(self):
        """ Test class Dog """
        self.assertEqual(Dog.__base__, Animal)

    def test_cat(self):
        """ Test class Cat """
        self.assertEqual(Cat.__base__, Animal)

    def test_catdog(self):
        """ Test class CatDog """
        assert Dog in CatDog.__bases__, 'Class Dog must be parent for class CatDog'
        assert Cat in CatDog.__bases__, 'Class Cat must be parent for class CatDog'

    def test_dogcat(self):
        """ Test class DogCat """
        assert Dog in DogCat.__bases__, 'Class Dog must be parent for class DogCat'
        assert Cat in DogCat.__bases__, 'Class Cat must be parent for class DogCat'
        assert 'info' in dir(DogCat), 'Метод info для класса DogCat должен быть реализован'
