from sympy import symbols, integrate, diff, solve
import numpy as np

t = symbols('t', real=True, positive=True)
v_t = -4*t**3 + 12*t**2

# 가속도가 k에서 12
a_t = diff(v_t, t)
eq = a_t.subs(t, symbols('k', positive=True, real=True)) - 12
k_vals = solve(eq, symbols('k', positive=True, real=True))
k = 1  # k = 1

# t = 3 ~ 4 구간에서 거리
distance_integral = integrate(v_t, (t, 3, 4))
distance = abs(float(distance_integral))

if abs(distance - 27.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')