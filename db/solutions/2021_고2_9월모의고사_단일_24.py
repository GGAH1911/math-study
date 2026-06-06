import sympy as sp
from sympy import log, sqrt, symbols, simplify, solve

# 기호 정의
b = symbols('b', real=True, positive=True)

# 주어진 조건: a = b^4
a = b**4

# 조건 검증: log_9(sqrt(a)) = log_3(b)
left_side = log(sqrt(a), 9)
right_side = log(b, 3)
condition_check = simplify(left_side - right_side)
print(f'조건 검증 (0이어야 함): {condition_check}')

# 구하는 값: 50 * log_b(sqrt(a))
result = 50 * log(sqrt(a), b)
result_simplified = simplify(result)
print(f'50 × log_b(sqrt(a)) = {result_simplified}')

if result_simplified == 100:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')