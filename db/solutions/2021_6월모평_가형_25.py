import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 곡선: x^3 - y^3 = e^(xy)
# 점 (a, 0)에서 a = 1 확인
a = 1
y = 0
result1 = a**3 - y**3 - np.exp(a*y)
print(f'Point (1,0) on curve: {abs(result1) < 1e-10}')

# 접선의 기울기 b = 3 확인
# 음함수 미분: dy/dx = (3x^2 - y*e^(xy)) / (3y^2 + x*e^(xy))
x_val, y_val = 1, 0
dy_dx = (3*x_val**2 - y_val*np.exp(x_val*y_val)) / (3*y_val**2 + x_val*np.exp(x_val*y_val))
b = dy_dx

print(f'Slope b = {b}')
print(f'a + b = {a + b}')

if abs(b - 3) < 1e-10 and a == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')