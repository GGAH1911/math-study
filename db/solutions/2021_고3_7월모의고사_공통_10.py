import numpy as np
from numpy import pi, sin, cos, arcsin

alpha = arcsin(1/3)
x1 = pi + alpha
x2 = 2*pi - alpha

def verify_equation(x):
    return 3*cos(x)**2 + 5*sin(x) - 1

val1 = verify_equation(x1)
val2 = verify_equation(x2)
sum_of_roots = x1 + x2

if abs(val1) < 1e-10 and abs(val2) < 1e-10 and abs(sum_of_roots - 3*pi) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')