import sys
import os
import unittest

# Add parent directory to Python path so 'src' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bmi_calculator import calculate_bmi, bmi_category, health_advice


class TestBMICalculator(unittest.TestCase):

    def test_calculate_bmi(self):
        self.assertEqual(calculate_bmi(70, 1.75), 22.86)

    def test_bmi_category(self):
        self.assertEqual(bmi_category(26), "Overweight")

    def test_health_advice(self):
        self.assertIn("balanced", health_advice(27))

    def test_invalid_height(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)


if __name__ == "__main__":
    unittest.main()
