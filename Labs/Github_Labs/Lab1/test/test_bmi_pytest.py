
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.bmi_calculator import calculate_bmi, bmi_category, health_advice

def test_calculate_bmi_normal():
    assert calculate_bmi(70, 1.75) == 22.86

def test_bmi_category():
    assert bmi_category(22.86) == "Normal"
    assert bmi_category(30) == "Obese"

def test_health_advice():
    assert "Maintain" in health_advice(22.5)
    assert "calorie" in health_advice(17.5)

def test_invalid_height():
    with pytest.raises(ValueError):
        calculate_bmi(70, 0)
