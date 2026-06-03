import sympy as sp
from sympy import symbols, diff, limit, Rational

x = symbols('x')
f_val_2 = Rational(1, 2)
f_prime_2 = Rational(-1, 6)
g_prime_2 = Rational(2, 3)

# 검증 1: g'(2) = 1 + 2*f'(2)
verify1 = 1 + 2 * f_prime_2
assert verify1 == g_prime_2, f'g\'(2) 계산 오류: {verify1} != {g_prime_2}'

# 검증 2: g'(2) = -4*f'(2)
verify2 = -4 * f_prime_2
assert verify2 == g_prime_2, f'로피탈 조건 오류: {verify2} != {g_prime_2}'

# 검증 3: 극한 조건
limit_value = g_prime_2 / (2 * f_prime_2)
assert limit_value == -2, f'극한값 오류: {limit_value} != -2'

print('VERIFY_PASS')