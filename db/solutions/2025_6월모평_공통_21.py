import numpy as np
from scipy.optimize import fsolve

def f(x):
    return x**4 - (8/3)*x**3 - 2*x**2 + 8*x

def f_prime(x):
    return 4*x**3 - 8*x**2 - 4*x + 8

# 조건 검증
assert abs(f(0)) < 1e-10, f'f(0) = {f(0)}'
assert abs(f_prime(1)) < 1e-10, f'f\'(1) = {f_prime(1)}'

# 조건 (가): f'(a) ≤ 0의 최댓값이 2
# f'(x) = 4(x+1)(x-1)(x-2)
# f'(x) ≤ 0 범위: (-∞, -1] ∪ [1, 2]
# 최댓값 = 2
assert f_prime(-1) == 0 and f_prime(1) == 0 and f_prime(2) == 0

# 조건 (나): f(x) = k의 해가 3개 이상인 최소 k = 8/3
f_at_2 = f(2)
expected_f2 = 8/3
assert abs(f_at_2 - expected_f2) < 1e-10, f'f(2) = {f_at_2}, expected = {expected_f2}'

# f(3) 계산
answer = f(3)
assert abs(answer - 15) < 1e-10, f'f(3) = {answer}'

print('VERIFY_PASS')