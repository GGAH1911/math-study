import sympy as sp
import numpy as np
from sympy import sqrt, cos, sin, symbols, pi, simplify

theta = -sp.acos(sp.Rational(-24, 25))
cos_theta = sp.Rational(-24, 25)
sin_theta = sp.Rational(7, 25)

cos_2theta = 2*cos_theta**2 - 1
sin_2theta = 2*sin_theta*cos_theta

print(f'cos(theta) = {cos_theta}')
print(f'sin(theta) = {sin_theta}')
print(f'cos(2*theta) = {cos_2theta}')
print(f'sin(2*theta) = {sin_2theta}')

P = (5*sqrt(2)*cos_theta, 5*sqrt(2)*sin_theta)
Q = (5*sqrt(2)*cos_2theta, 5*sqrt(2)*sin_2theta)
A = (-5*sqrt(2), 0)
B = (5*sqrt(2), 0)

PA = (A[0] - P[0], A[1] - P[1])
QB = (B[0] - Q[0], B[1] - Q[1])

PA_dot_QB = PA[0]*QB[0] + PA[1]*QB[1]
PA_dot_QB_simplified = simplify(PA_dot_QB)

print(f'PA · QB = {PA_dot_QB_simplified}')

PA_dot_QB_num = sp.nsimplify(PA_dot_QB_simplified)
print(f'PA · QB (simplified) = {PA_dot_QB_num}')

abs_PA_dot_QB = abs(PA_dot_QB_simplified)
print(f'|PA · QB| = {abs_PA_dot_QB}')

PB_squared = (B[0]-P[0])**2 + (B[1]-P[1])**2
PB = sqrt(PB_squared)
print(f'|PB| = {simplify(PB)}')

if abs(float(simplify(PB)) - 14) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')