from sympy import symbols, Eq, solve
import math

# 파라미터
d = 2
k = 3/2

# (1) 2^d = kd + 1 검증
assert abs(2**d - (k*d + 1)) < 1e-9

# (2) a_n = 2n - 1 검증
a1 = 2*1 - 1  # a_1 = 1
a3 = 2*3 - 1  # a_3 = 5
assert a1 == 1 and a3 == 5

# (3) A_n = (kd²/2) * 2^(a_n) 검증
A1 = (k * d**2 / 2) * (2**a1)
A3 = (k * d**2 / 2) * (2**a3)
assert abs(A3 / A1 - 16) < 1e-9

# (4) 최종 답 검증
p = d
f_2 = 2*2 - 1  # f(2) = 3
g_4 = (k * d**2 / 2) * (2**(2*4 - 1))  # g(4) = 3 * 2^7
result = p + g_4 / f_2
assert abs(result - 130) < 1e-9

print('VERIFY_PASS')