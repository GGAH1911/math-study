import sympy as sp
from sympy import log, simplify

# 원래 식 계산
result = log(36, 3) - log(4, 3)
result_simplified = simplify(result)

# 로그의 성질을 이용한 계산
alternative = log(36/4, 3)
alternative_simplified = simplify(alternative)

# log_3(9) = log_3(3^2) = 2
expected = 2

# 수치 검증
numerical_result = float(result_simplified)

if abs(numerical_result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')