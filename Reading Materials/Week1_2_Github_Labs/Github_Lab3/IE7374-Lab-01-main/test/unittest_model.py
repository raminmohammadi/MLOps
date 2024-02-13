import sys
import os
import unittest
import random
import numpy as np
import src.calculator as calculator
import src.lab1 as model

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

seed = 42
random.seed(seed)


class TestLab1(unittest.TestCase):

    def test_random_data(self):
        X, y = model.generate_random_data()
        self.assertEqual(X.shape, (1000, 4))
        self.assertEqual(y.shape, (1000,))

    def test_fun2(self):
        a = random.random()
        b = random.random()
        l = []
        l.append(calculator.fun1(a, b))
        l.append(calculator.fun2(a, b))
        l.append(calculator.fun3(a, b))
        l.append(calculator.fun4(l[0], l[1], l[2]))
        l = np.array(l)
        print(l)
        k = model.scale_input(l)
        for i in k:
            self.assertTrue(0 <= i <= 1)

    def test_fun3(self):
        y_pred = model.main()
        self.assertTrue(y_pred == 0 or y_pred == 1)


if __name__ == '__main__':
    unittest.main()
