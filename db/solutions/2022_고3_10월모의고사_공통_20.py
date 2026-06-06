import numpy as np
from scipy.optimize import fsolve

# f(x) = x^3 + 4x^2 + 1
# 조건 (나) 검증: xf(x) >= -4x^2 + x

def verify():
    a = 4
    
    # 조건 (나) 확인: x^2(x^2 + ax + 4) >= 0
    # x^2 + 4x + 4 = (x+2)^2 >= 0 ✓
    for x in np.linspace(-10, 10, 100):
        lhs = x * (x**3 + a*x**2 + 1)
        rhs = -4*x**2 + x
        if lhs < rhs - 1e-10:
            return 'VERIFY_FAIL'
    
    # f(5) 계산
    f_5 = 5**3 + a*5**2 + 1
    if f_5 == 226:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()