import src.lab1 as model
import random
import numpy as np
import src.calculator as calculator
seed = 42
random.seed(seed)

def test_random_data_gen():
    X, y = model.generate_random_data()
    assert X.shape == (1000, 4)
    assert y.shape == (1000,)


def test_input_scaling():
    a = random.random()
    b = random.random()
    l = []
    l.append(calculator.fun1(a, b))
    l.append(calculator.fun2(a, b))
    l.append(calculator.fun3(a, b))
    l.append(calculator.fun4(l[0], l[1], l[2]))
    l = np.array(l)
    print(l)
    input = model.scale_input(l)
    for i in input:
        assert 0 <= i <= 1


def test_prediction():
    y_pred = model.main()
    assert y_pred == 0 or y_pred == 1