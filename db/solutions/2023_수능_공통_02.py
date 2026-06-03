import sympy as sp
import numpy as np

x = sp.Symbol('x', real=True, positive=True)
expr = (sp.sqrt(x**2 - 2) + 3*x) / (x + 5)

# 극한 계산
limit_result = sp.limit(expr, x, sp.oo)

if limit_result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')