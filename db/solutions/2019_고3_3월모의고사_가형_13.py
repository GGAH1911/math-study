import sympy as sp
import numpy as np

# a = 1을 구했으므로 검증
a = 1

# Step 1: a 값 검증 (연속성)
x = sp.Symbol('x')
f_expr = 2*sp.sin(x) + a
limit_val = sp.limit(f_expr, x, sp.pi/2)
f_at_pi2 = 3*a
assert limit_val == f_at_pi2, f'Continuity check failed: {limit_val} != {f_at_pi2}'

# Step 2: 최댓값과 최솟값
# f(x) = 2*sin(x) + 1
# sin(x)는 [0, pi]에서 [0, 1] 범위
max_sin = 1  # x = pi/2
min_sin = 0  # x = 0 또는 x = pi

f_max = 2 * max_sin + 1
f_min = 2 * min_sin + 1

# 검증
assert f_max == 3, f'Max value should be 3, got {f_max}'
assert f_min == 1, f'Min value should be 1, got {f_min}'

result_sum = f_max + f_min
assert result_sum == 4, f'Sum should be 4, got {result_sum}'

print('VERIFY_PASS')