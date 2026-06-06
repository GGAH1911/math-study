import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 함수 정의
def f(x):
    return abs(x**2 - 3) - 2*x

def g(x):
    return -x + 3

# [0, 3]에서 넓이 계산
# [0, sqrt(3)]: g(x) - f(x) = x^2 + x
# [sqrt(3), 3]: g(x) - f(x) = -x^2 + x + 6

sqrt3 = np.sqrt(3)

# 첫 번째 적분
int1 = (sqrt3**3/3 + sqrt3**2/2) - 0

# 두 번째 적분
int2 = (-27/3 + 9/2 + 18) - (-sqrt3**3/3 + 3/2 + 6*sqrt3)

total_area = int1 + int2
expected_area = 27/2 - 4*sqrt3

# 교점 확인
x1, x2, x3, x4 = -2, -1, 0, 3
assert abs(f(x1) - g(x1)) < 1e-10
assert abs(f(x2) - g(x2)) < 1e-10
assert abs(f(x3) - g(x3)) < 1e-10
assert abs(f(x4) - g(x4)) < 1e-10
assert x4 - x1 == 5

# 넓이 검증
assert abs(total_area - expected_area) < 1e-10

p = 27/2
q = 4
result = p * q
assert abs(result - 54) < 1e-10

print('VERIFY_PASS')