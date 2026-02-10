import pytest
from src.calculator import add, subtract, multiply, divide
import math

def test_add_zero():
    assert add(0, 0) == 0
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_large_numbers():
    assert add(1000000, 2000000) == 3000000

def test_subtract_zero():
    assert subtract(0, 0) == 0
    assert subtract(5, 0) == 5
    assert subtract(0, 5) == -5

def test_subtract_large_numbers():
    assert subtract(2000000, 1000000) == 1000000

def test_multiply_zero():
    assert multiply(0, 5) == 0
    assert multiply(5, 0) == 0
    assert multiply(0, 0) == 0

def test_multiply_large_numbers():
    assert multiply(1000, 2000) == 2000000

def test_divide_zero():
    assert divide(0, 1) == 0
    assert divide(0, -1) == 0

def test_divide_large_numbers():
    assert divide(1000000, 2) == 500000

def test_divide_remainder():
    assert divide(5, 2) == pytest.approx(2.5)

def test_divide_by_negative_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, -0.0)

def test_add_very_small_floats():
    assert add(1e-10, 2e-10) == pytest.approx(3e-10)

def test_subtract_very_small_floats():
    assert subtract(2e-10, 1e-10) == pytest.approx(1e-10)

def test_multiply_very_small_floats():
    assert multiply(1e-10, 2e-10) == pytest.approx(2e-20)

def test_divide_very_small_floats():
    assert divide(1e-10, 2e-10) == pytest.approx(0.5)

def test_add_very_large_floats():
    assert add(1e10, 2e10) == pytest.approx(3e10)

def test_subtract_very_large_floats():
    assert subtract(2e10, 1e10) == pytest.approx(1e10)

def test_multiply_very_large_floats():
    assert multiply(1e10, 2e10) == pytest.approx(2e20)

def test_divide_very_large_floats():
    assert divide(2e10, 1e10) == pytest.approx(2.0)

def test_divide_by_very_small_number():
    assert divide(1, 1e-10) == pytest.approx(1e10)

def test_divide_by_very_large_number():
    assert divide(1, 1e10) == pytest.approx(1e-10)

def test_add_infinity():
    assert add(float('inf'), 1) == float('inf')
    assert add(float('-inf'), 1) == float('-inf')
    assert math.isnan(add(float('inf'), float('-inf')))

def test_subtract_infinity():
    assert subtract(float('inf'), 1) == float('inf')
    assert subtract(float('-inf'), 1) == float('-inf')
    assert subtract(float('inf'), float('-inf')) == float('inf')

def test_multiply_infinity():
    assert multiply(float('inf'), 2) == float('inf')
    assert multiply(float('-inf'), 2) == float('-inf')
    assert multiply(float('inf'), float('-inf')) == float('-inf')

def test_divide_infinity():
    assert divide(float('inf'), 2) == float('inf')
    assert divide(float('-inf'), 2) == float('-inf')
    assert divide(1, float('inf')) == 0.0
    assert divide(1, float('-inf')) == -0.0

def test_divide_infinity_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0.0)

def test_add_nan():
    assert math.isnan(add(float('nan'), 1))
    assert math.isnan(add(float('nan'), float('nan')))

def test_subtract_nan():
    assert math.isnan(subtract(float('nan'), 1))
    assert math.isnan(subtract(float('nan'), float('nan')))

def test_multiply_nan():
    assert math.isnan(multiply(float('nan'), 1))
    assert math.isnan(multiply(float('nan'), float('nan')))

def test_divide_nan():
    assert math.isnan(divide(float('nan'), 1))
    assert math.isnan(divide(1, float('nan')))

def test_divide_nan_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(float('nan'), 0)

def test_add_type_error():
    with pytest.raises(TypeError):
        add("1", 2)
    with pytest.raises(TypeError):
        add([], 2)

def test_subtract_type_error():
    with pytest.raises(TypeError):
        subtract("1", 2)
    with pytest.raises(TypeError):
        subtract([], 2)

def test_multiply_type_error():
    with pytest.raises(TypeError):
        multiply("1", 2)
    with pytest.raises(TypeError):
        multiply([], 2)

def test_divide_type_error():
    with pytest.raises(TypeError):
        divide("1", 2)
    with pytest.raises(TypeError):
        divide([], 2)
