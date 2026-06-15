from sympy import *

# 주어진 식: 5^0 × 25^(1/2)
result = 5**0 * 25**(Rational(1, 2))
print(f'계산 결과: {result}')

# 답이 5인지 확인
if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')