# test_pytest.py
from area_calculator import (
    square_area, square_perimeter,
    rectangle_area, rectangle_perimeter,
    triangle_area, triangle_perimeter,
    parallelogram_area, parallelogram_perimeter
)
import pytest
import sys
import os

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "src")))


# Square

@pytest.mark.parametrize("side, expected_area, expected_perim", [
    (4, 16, 16),
    (0, 0, 0),
    (2.5, 6.25, 10),
])
def test_square(side, expected_area, expected_perim):
    assert square_area(side) == pytest.approx(expected_area)
    assert square_perimeter(side) == pytest.approx(expected_perim)

# Rectangle


@pytest.mark.parametrize("length,width,expected_area,expected_perim", [
    (5, 3, 15, 16),
    (0, 10, 0, 20),
    (2.5, 4.0, 10.0, 13.0),
])
def test_rectangle(length, width, expected_area, expected_perim):
    assert rectangle_area(length, width) == pytest.approx(expected_area)
    assert rectangle_perimeter(length, width) == pytest.approx(expected_perim)

# Triangle


@pytest.mark.parametrize("base,height,a,b,c,expected_area,expected_perim", [
    (6, 4, 3, 4, 5, 12.0, 12),   # classic 3-4-5 triangle
    (0, 5, 0, 0, 0, 0.0, 0),     # degenerate
    (2.5, 4.0, 1.0, 1.5, 2.0, 5.0, 4.5),
])
def test_triangle(base, height, a, b, c, expected_area, expected_perim):
    assert triangle_area(base, height) == pytest.approx(expected_area)
    assert triangle_perimeter(a, b, c) == pytest.approx(expected_perim)

# Parallelogram


@pytest.mark.parametrize("base,height,a,b,expected_area,expected_perim", [
    (6, 4, 6, 4, 24, 20),
    (0, 5, 0, 0, 0, 0),
    (2.5, 3.0, 2.5, 3.0, 7.5, 11.0),
])
def test_parallelogram(base, height, a, b, expected_area, expected_perim):
    assert parallelogram_area(base, height) == pytest.approx(expected_area)
    assert parallelogram_perimeter(a, b) == pytest.approx(expected_perim)

# Quick smoke test to ensure all functions are callable


def test_smoke():
    assert callable(square_area)
    assert callable(rectangle_area)
    assert callable(triangle_area)
    assert callable(parallelogram_area)
