import sympy as sp
from sympy import sqrt, Rational

# P 좌표
x_p, y_p = Rational(-7, 5), Rational(24, 5)

# 검증 1: P가 C1 위에 있는가
C1_check = x_p**2 - y_p**2/24
assert C1_check == 1, f'P on C1 failed: {C1_check}'

# 검증 2: |PF| = 8, |PF'| = 6
PF_squared = (x_p - 5)**2 + y_p**2
PF_prime_squared = (x_p + 5)**2 + y_p**2
assert PF_squared == 64, f'|PF|^2 failed: {PF_squared}'
assert PF_prime_squared == 36, f'|PF\'-|^2 failed: {PF_prime_squared}'

# Q 좌표
x_q, y_q = Rational(-62, 25), Rational(84, 25)

# 검증 3: Q가 C2 위에 있는가
C2_check = x_q**2/4 - y_q**2/21
assert C2_check == 1, f'Q on C2 failed: {C2_check}'

# 검증 4: |QF| - |QF'| = 4
QF_squared = (x_q - 5)**2 + y_q**2
QF_prime_squared = (x_q + 5)**2 + y_q**2
QF = sqrt(QF_squared)
QF_prime = sqrt(QF_prime_squared)
assert QF - QF_prime == 4, f'|QF| - |QF\'-| failed'

# 검증 5: P, Q, F' 일직선
slope_PF_prime = y_p / (x_p + 5)
slope_QF_prime = y_q / (x_q + 5)
assert slope_PF_prime == slope_QF_prime, f'P, Q, F\' collinearity failed'

# 기울기 m
m = (y_q - y_p) / (x_q - x_p)
assert m == Rational(4, 3), f'Gradient failed: {m}'

# 답
result = 60 * m
assert result == 80, f'60m failed: {result}'

print('VERIFY_PASS')