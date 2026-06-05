import numpy as np
from sympy import *

# a = -4인 경우 검증
a = -4
c = 1

# F(c) = c^4 + (a/3)*c^3
F_c = c**4 + (a/3)*c**3
assert abs(F_c - (-1/3)) < 1e-10, f'F(c) = {F_c}, expected -1/3'

# x=c에서 연속성 확인
F_c_plus_5 = F_c + 5
abs_part = abs(F_c - 13/3)
assert abs(F_c_plus_5 - abs_part) < 1e-10, f'Continuity failed: {F_c_plus_5} != {abs_part}'

# F(1) 계산
F_1 = 1**4 + (a/3)*(1**3)
assert abs(F_1 - (-1/3)) < 1e-10, f'F(1) = {F_1}'

# g(1) 계산 (x=1 >= c=1)
g_1 = abs(F_1 - 13/3)
expected_g_1 = 14/3
assert abs(g_1 - expected_g_1) < 1e-10, f'g(1) = {g_1}, expected {expected_g_1}'

print('VERIFY_PASS')