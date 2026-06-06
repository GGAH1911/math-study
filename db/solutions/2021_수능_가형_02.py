import numpy as np
from sympy import *

n = symbols('n', positive=True, real=True)

# 원래 함수
f = 1 / (sqrt(4*n**2 + 2*n + 1) - 2*n)

# 극한값 계산
limit_val = limit(f, n, oo)

print(f'극한값: {limit_val}')

if limit_val == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')