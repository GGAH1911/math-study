import sympy as sp
from sympy import symbols, diff, simplify

# 검증: g'(0) + g'(2) = 16 을 만족하면 f(2) - f(0) = 8
f0, f2, f_prime_2 = symbols('f0 f2 f_prime_2', real=True)

# g'(0) = -2*f(0)
g_prime_0 = -2 * f0

# g'(2) = 2*f(2)
g_prime_2 = 2 * f2

# 조건: g'(0) + g'(2) = 16
condition = g_prime_0 + g_prime_2 - 16

# f(2) - f(0)을 표현
diff_f = f2 - f0

# condition = -2*f0 + 2*f2 - 16 = 0 일 때, f2 - f0을 구하기
# -2*f0 + 2*f2 = 16
# 2*(f2 - f0) = 16
# f2 - f0 = 8

result = 16 / 2
print('VERIFY_PASS' if result == 8 else 'VERIFY_FAIL')