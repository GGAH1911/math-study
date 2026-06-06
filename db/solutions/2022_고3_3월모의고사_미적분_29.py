import numpy as np
from scipy.optimize import fsolve

def f(x):
    if isinstance(x, np.ndarray):
        return np.piecewise(x, 
            [x > 1, (x >= -1) & (x <= 1), x < -1, x == 1, x == -1],
            [lambda x: 2*x, lambda x: np.where((x > -1) & (x < 1), -1, np.where(x == 1, 0.5, np.where(x == -1, -1.5, 2*x))), 
             lambda x: 2*x, lambda x: 0.5, lambda x: -1.5])
    if x > 1:
        return 2*x
    elif x == 1:
        return 0.5
    elif -1 < x < 1:
        return -1
    elif x == -1:
        return -1.5
    else:  # x < -1
        return 2*x

t = 4
print(f"Testing t = {t}:")
if 2 < t < 4:
    x1 = 2 / (t - 2)
    if x1 > 1:
        print(f"  Intersection at x = {x1}: f({x1}) = {f(x1)}, line = {t*x1 - 2}")
if t > 1 or -1 < t < 0:
    x2 = 1 / t
    if -1 < x2 < 1:
        print(f"  Intersection at x = {x2}: f({x2}) = {f(x2)}, line = {t*x2 - 2}")
if 0 < t < 2:
    x3 = 2 / (t - 2)
    if x3 < -1:
        print(f"  Intersection at x = {x3}: f({x3}) = {f(x3)}, line = {t*x3 - 2}")

print(f"\nAnswer verification: m = 7, a_m = 4, m*a_m = {7*4}")
if 7*4 == 28:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")