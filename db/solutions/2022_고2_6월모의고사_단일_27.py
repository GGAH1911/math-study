import numpy as np
from scipy.optimize import fsolve

# a^(3/2) = 7/2 에서
a = (7/2)**(2/3)

xA = 3/2
xB = 7/2
xC = 9/2

# A 검증: a^xA = -xA + 5
val_A = a**xA
line_A = -xA + 5
assert abs(val_A - line_A) < 1e-10, f'A 실패: {val_A} vs {line_A}'

# B 검증: log_a(xB) = -xB + 5
val_B = np.log(xB) / np.log(a)
line_B = -xB + 5
assert abs(val_B - line_B) < 1e-10, f'B 실패: {val_B} vs {line_B}'

# C 검증: log_a(xC-1) - 1 = -xC + 5
val_C = np.log(xC - 1) / np.log(a) - 1
line_C = -xC + 5
assert abs(val_C - line_C) < 1e-10, f'C 실패: {val_C} vs {line_C}'

# 거리 비 검증
AB_dist = (xB - xA) * np.sqrt(2)
BC_dist = (xC - xB) * np.sqrt(2)
ratio = AB_dist / BC_dist
assert abs(ratio - 2.0) < 1e-10, f'거리비 실패: {ratio}'

# 최종 답
answer = 4 * a**3
assert abs(answer - 49) < 1e-10, f'답 실패: {answer}'
print('VERIFY_PASS')