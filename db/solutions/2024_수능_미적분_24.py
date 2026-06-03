import math
from sympy import *

# 매개변수 정의
t = symbols('t', real=True, positive=True)

# 원래 함수
x_func = ln(t**3 + 1)
y_func = sin(pi * t)

# 도함수 계산
dx_dt = diff(x_func, t)
dy_dt = diff(y_func, t)

print(f'dx/dt = {dx_dt}')
print(f'dy/dt = {dy_dt}')

# dy/dx = (dy/dt) / (dx/dt)
dy_dx = dy_dt / dx_dt

print(f'dy/dx = {dy_dx}')

# t=1 에서의 값
t_val = 1
result = dy_dx.subs(t, t_val)

print(f'dy/dx at t=1: {result}')
print(f'Numerical value: {float(result)}')

# 정답 확인
expected = -2*pi/3
print(f'Expected: {expected}')
print(f'Expected numerical: {float(expected)}')

if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')