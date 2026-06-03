from sympy import *
import numpy as np

# 원래 식: (5 / (25^(1/3)))^(3/2)
result = (5 / (25**(Rational(1,3))))**(Rational(3,2))
result_simplified = simplify(result)

# 정답이 sqrt(5)인지 확인
expected = sqrt(5)
verification = simplify(result_simplified - expected) == 0

if verification:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')