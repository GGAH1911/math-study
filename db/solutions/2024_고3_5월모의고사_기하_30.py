import numpy as np
from scipy.optimize import fsolve

# c^2 = 6/5
c_squared = 6/5
c = np.sqrt(c_squared)
a1 = 4 * c

# b1^2 = a1^2 - c^2
b1_squared = a1**2 - c_squared

# a2, c2, b2
a2 = (a1 + 3*c) / 2
c2 = (a1 - c) / 2
b2_squared = a2**2 - c2**2

# 검증 1: 단축 길이
assert np.isclose(b2_squared, 12), f'b2^2 = {b2_squared}, expected 12'

# 검증 2: c(a1 + c) = 6
assert np.isclose(c * (a1 + c), 6), f'c(a1+c) = {c*(a1+c)}, expected 6'

# B는 E1과 E2의 교점
# E1: x^2/a1^2 + y^2/b1^2 = 1
# E2 (중심 (a1+c)/2): (x-(a1+c)/2)^2/a2^2 + y^2/b2^2 = 1

def equations(vars):
    x, y = vars
    # E1
    eq1 = x**2/a1**2 + y**2/b1_squared - 1
    # E2
    eq2 = (x - (a1+c)/2)**2/a2**2 + y**2/b2_squared - 1
    return [eq1, eq2]

# y > 0인 교점 찾기
sol = fsolve(equations, [a1/2, 2])
x_B, y_B = sol

if y_B < 0:
    sol = fsolve(equations, [a1/2, -2])
    x_B, y_B = sol

# BF', BA, AF' 계산
BF_prime = np.sqrt((x_B + c)**2 + y_B**2)
BA = np.sqrt((x_B - a1)**2 + y_B**2)
AF_prime = a1 + c

# 조건 검증
diff = BF_prime - BA
expected = AF_prime / 5

if np.isclose(diff, expected, atol=1e-10):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {diff} vs {expected}')