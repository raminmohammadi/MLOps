# test_unittest.py
import unittest
import sys
import os

# Add src/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from area_calculator import (
    square_area, square_perimeter,
    rectangle_area, rectangle_perimeter,
    triangle_area, triangle_perimeter,
    parallelogram_area, parallelogram_perimeter
)

class TestShapes(unittest.TestCase):

    # Square
    def test_square_basic(self):
        self.assertAlmostEqual(square_area(4), 16)
        self.assertAlmostEqual(square_perimeter(4), 16)

    def test_square_edge(self):
        self.assertAlmostEqual(square_area(0), 0)
        self.assertAlmostEqual(square_perimeter(0), 0)
        self.assertAlmostEqual(square_area(2.5), 6.25)

    # Rectangle
    def test_rectangle_basic(self):
        self.assertAlmostEqual(rectangle_area(5, 3), 15)
        self.assertAlmostEqual(rectangle_perimeter(5, 3), 16)

    def test_rectangle_float(self):
        self.assertAlmostEqual(rectangle_area(2.5, 4.0), 10.0)
        self.assertAlmostEqual(rectangle_perimeter(2.5, 4.0), 13.0)

    # Triangle
    def test_triangle_basic(self):
        self.assertAlmostEqual(triangle_area(6, 4), 12.0)
        self.assertAlmostEqual(triangle_perimeter(3, 4, 5), 12)

    def test_triangle_degenerate(self):
        self.assertAlmostEqual(triangle_area(0, 5), 0.0)
        self.assertAlmostEqual(triangle_perimeter(0, 0, 0), 0)

    # Parallelogram
    def test_parallelogram_basic(self):
        self.assertAlmostEqual(parallelogram_area(6, 4), 24)
        self.assertAlmostEqual(parallelogram_perimeter(6, 4), 20)

    def test_parallelogram_float(self):
        self.assertAlmostEqual(parallelogram_area(2.5, 3.0), 7.5)
        self.assertAlmostEqual(parallelogram_perimeter(2.5, 3.0), 11.0)

if __name__ == "__main__":
    unittest.main()
