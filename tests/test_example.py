import pytest

# Example test with pytest.raises to handle exceptions
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# Parameterized test example using pytest.mark.parametrize
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (2, 3, 5),
    (3, 5, 8),
])
def test_addition(a, b, expected):
    assert a + b == expected
