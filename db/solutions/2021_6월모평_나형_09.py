import numpy as np
from sympy import *

x = symbols('x', real=True)
f = 2**Abs(x)

# 구간 [-1, 3]에서 샘플링
samples = np.linspace(-1, 3, 1000)
values = [float(f.subs(x, xi)) for xi in samples]

max_val = max(values)
min_val = min(values)

# 경계점 확인
f_neg1 = float(2**1)
f_0 = float(2**0)
f_3 = float(2**3)

max_exact = max(f_neg1, f_0, f_3)
min_exact = min(f_neg1, f_0, f_3)

sum_result = max_exact + min_exact

if abs(sum_result - 9) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')