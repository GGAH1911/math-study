from sympy import *
import math

# 원래 문제식을 정확히 표현
result = cbrt(9) * (3**Rational(-5, 3))

# 계산
result_simplified = simplify(result)
print(f'Simplified result: {result_simplified}')

# 수치 검증
result_numeric = float(result_simplified)
expected = 1/3

if abs(result_numeric - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')