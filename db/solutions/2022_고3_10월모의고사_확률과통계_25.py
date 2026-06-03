import numpy as np
from fractions import Fraction

# 원래 문제의 조건: a = 2
a = 2

# X의 확률분포
X_values = np.array([-3, 0, a])
P_values = np.array([Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)])

# E(X) 계산
E_X = sum(x * p for x, p in zip(X_values, P_values))
print(f'E(X) = {E_X}')
assert E_X == -1, f'E(X) should be -1 but got {E_X}'

# E(X^2) 계산
E_X2 = sum(x**2 * p for x, p in zip(X_values, P_values))
print(f'E(X^2) = {E_X2}')

# V(X) 계산
V_X = E_X2 - E_X**2
print(f'V(X) = {V_X}')

# V(aX) = a^2 * V(X) 계산
V_aX = a**2 * V_X
print(f'V({a}X) = {V_aX}')

# 답 검증
if V_aX == 18:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected 18, got {V_aX}')