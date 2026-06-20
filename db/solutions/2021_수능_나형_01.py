from sympy import *

# 계산
result = 3**0 * 8**(Rational(2,3))
print(f'Result: {result}')

# 수치 검증
result_numeric = float(result)
print(f'Numeric: {result_numeric}')

if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')