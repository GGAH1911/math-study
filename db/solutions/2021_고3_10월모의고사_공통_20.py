import numpy as np
from scipy.optimize import fsolve

def f(x):
    return x**3 - 3*x**2 + 2*x

def g(x):
    return -6*x**2

intersect_x = np.array([-2, -1, 0])
for x_val in intersect_x:
    assert abs(f(x_val) - g(x_val)) < 1e-10, f"Intersection failed at x={x_val}"

from scipy.integrate import quad

area1 = quad(lambda x: f(x) - g(x), -2, -1)[0]
area2 = quad(lambda x: g(x) - f(x), -1, 0)[0]
total_area = area1 + area2
result_4S = 4 * total_area

assert abs(result_4S - 2.0) < 1e-9, f"Expected 4S=2, got {result_4S}"
print('VERIFY_PASS')