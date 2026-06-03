import numpy as np
from sympy import log as sym_log, simplify, Rational

# 정답 검증: 10^10
product = 10**10

# 각 a 값 검증
a_values = [10**(Rational(4,3)), 10**(Rational(10,3)), 10**(Rational(16,3))]

for i, a in enumerate(a_values, 1):
    # 범위 확인
    log_a = float(Rational(6*i-2, 3))
    assert 0.5 < log_a < 5.5, f'n={i}: 범위 조건 위배'
    
    # 자연수 조건 확인
    value = Rational(1,3) + Rational(1,2) * Rational(6*i-2, 3)
    assert value == i, f'n={i}: 자연수 아님'

# 곱 검증
product_exponents = Rational(4,3) + Rational(10,3) + Rational(16,3)
assert product_exponents == 10, 'VERIFY_FAIL'

print('VERIFY_PASS')