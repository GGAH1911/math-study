import numpy as np

# 유도된 상수
a = -3
b = 0

# 조건 (나) f(4) = 2 검증
x = 4
lhs_factor = np.sqrt(2*x + 1) - 1  # sqrt(9) - 1 = 2
rhs = x**2 + a*x + b  # 16 - 12 + 0 = 4
f_4 = rhs / lhs_factor  # 4 / 2 = 2

# f(0) = a = -3 검증
f_0 = a

if np.isclose(f_4, 2.0) and np.isclose(f_0, -3.0):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')