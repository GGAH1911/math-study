from sympy import *
import math

# 원래 식: sqrt[4]{25^2} × sqrt[4]{5^4}
result = (25**2)**(1/4) * (5**4)**(1/4)
answer = 25

# 검증
if abs(result - answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')