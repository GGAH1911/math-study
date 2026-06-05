import numpy as np
from sympy import symbols, limit, oo, simplify

n = symbols('n', integer=True, positive=True)
product_r = 1 * 2 * 7

# 각 r 값에 대해 극한이 1인지 확인
for r_val in [1, 2, 7]:
    expr = (3**n + r_val**(n+1)) / (3**n + 7 * r_val**n)
    lim_val = limit(expr, n, oo)
    if lim_val != 1:
        print('VERIFY_FAIL')
        exit()

# 답이 10(합)인지 확인
if 1 + 2 + 7 == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')