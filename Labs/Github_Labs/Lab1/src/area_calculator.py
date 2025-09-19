"""
shapes.py
Simple geometry functions for basic shapes.
Useful as a starting point for MLOps labs (easy unit tests, reproducibility).
"""

# -----------------------------
# Square
# -----------------------------


def square_area(side: float) -> float:
    """Return area of a square given side length."""
    return side * side


def square_perimeter(side: float) -> float:
    """Return perimeter of a square given side length."""
    return 4 * side


# -----------------------------
# Rectangle
# -----------------------------
def rectangle_area(length: float, width: float) -> float:
    """Return area of a rectangle given length and width."""
    return length * width


def rectangle_perimeter(length: float, width: float) -> float:
    """Return perimeter of a rectangle given length and width."""
    return 2 * (length + width)


# -----------------------------
# Triangle
# -----------------------------
def triangle_area(base: float, height: float) -> float:
    """Return area of a triangle given base and height."""
    return 0.5 * base * height


def triangle_perimeter(a: float, b: float, c: float) -> float:
    """Return perimeter of a triangle given three side lengths."""
    return a + b + c


# -----------------------------
# Parallelogram
# -----------------------------
def parallelogram_area(base: float, height: float) -> float:
    """Return area of a parallelogram given base and height."""
    return base * height


def parallelogram_perimeter(a: float, b: float) -> float:
    """Return perimeter of a parallelogram given two adjacent side lengths."""
    return 2 * (a + b)


# -----------------------------
# Quick demo (runs only if you execute this file directly)
# -----------------------------
if __name__ == "__main__":
    print("Square: area =", square_area(4),
          ", perimeter =", square_perimeter(4))
    print("Rectangle: area =", rectangle_area(5, 3),
          ", perimeter =", rectangle_perimeter(5, 3))
    print("Triangle: area =", triangle_area(6, 4),
          ", perimeter =", triangle_perimeter(3, 4, 5))
    print("Parallelogram: area =", parallelogram_area(6, 4),
          ", perimeter =", parallelogram_perimeter(6, 4))
