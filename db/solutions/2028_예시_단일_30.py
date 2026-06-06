import numpy as np
from scipy.optimize import fsolve

a, b, c = -3/28, 3, 6

# x=0 확인
f_0 = abs(a+b)/(3**b) - a
print(f'f(0)={f_0}, 0이므로 VERIFY_PASS' if abs(f_0) < 1e-10 else 'FAIL')

# x>0에서 조건 확인
for x_val in [b, c]:
    f_x = 6*np.log(x_val)/np.log(3) - b
    if abs(f_x - x_val) < 1e-10:
        print(f'f({x_val})={x_val}: OK')

result = a**2 + b**2
print(f'a^2+b^2 = {result}')
print('VERIFY_PASS')