import numpy as np
from scipy.optimize import fsolve

a = -0.25
b = -2

def f(x):
    return a * (x - b)**2

f4 = f(4)
f6 = f(6)
result = f4 * f6

print(f'f(4) = {f4}')
print(f'f(6) = {f6}')
print(f'f(4) × f(6) = {result}')

if abs(result - 144) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')