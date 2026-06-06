import sympy as sp
from sympy import log, symbols, solve, simplify

# 변수 정의
t = sp.Rational(1, 2)

# 주어진 조건 확인
log_a_b = t
log_b_c = 2*t
log_c_a = 4*t

# 로그 곱의 성질 검증: log_a(b) * log_b(c) * log_c(a) = 1
product = log_a_b * log_b_c * log_c_a
assert product == 1, f'Product should be 1, got {product}'

# 주어진 등식 검증
assert log_a_b == log_b_c / 2, 'First equality failed'
assert log_a_b == log_c_a / 4, 'Second equality failed'

# 최종 답 계산
answer = log_a_b + log_b_c + log_c_a
assert answer == sp.Rational(7, 2), f'Answer should be 7/2, got {answer}'

print('VERIFY_PASS')