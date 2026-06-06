from sympy import *
import numpy as np

# 원래 문제: $\sqrt[3]{2} \times 2^{2/3}$의 값
result = 2**(Rational(1,3)) * 2**(Rational(2,3))
result_simplified = simplify(result)

print(f'Result: {result_simplified}')
print(f'Numerical: {float(result_simplified)}')

if result_simplified == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')