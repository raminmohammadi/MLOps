def calculate_bmi(weight_kg, height_m):
    """Calculate BMI given weight in kilograms and height in meters."""
    if height_m <= 0:
        raise ValueError("Height must be positive.")
    return round(weight_kg / (height_m ** 2), 2)


def bmi_category(bmi):
    """Return BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def health_advice(bmi):
    """Return simple advice based on BMI category."""
    category = bmi_category(bmi)
    if category == "Underweight":
        return "Increase your calorie intake."
    elif category == "Normal":
        return "Maintain your current lifestyle."
    elif category == "Overweight":
        return "Consider a balanced diet and exercise."
    else:
        return "Consult a healthcare provider."
