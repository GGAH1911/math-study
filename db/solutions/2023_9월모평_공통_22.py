import numpy as np
from scipy.optimize import fsolve

def f(x):
    return x**3 - 12*x**2 + 45*x - 46

# 검증
print('f(3) =', f(3), '(극댓값 8 확인)')
print('f(8) =', f(8))

# 도함수
def f_prime(x):
    return 3*x**2 - 24*x + 45

# 극값점
roots_prime = np.roots([3, -24, 45])
print('극값점:', roots_prime)
print('f(5) =', f(5))

if f(8) == 58:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')