from operation import my_sum, div, mul, sub


def test_sum():
    assert my_sum(3, 5) == 8
    assert my_sum(3, 3) == 6
    assert my_sum(3, 7) == 10


def test_mul():
    assert mul(3, 5) == 15


def test_sub():
    assert sub(3, 5) == -2
