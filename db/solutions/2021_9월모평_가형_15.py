import numpy as np
from sympy import *

# 정의역에서 f(x) = ln((sec(x) + tan(x))/a)
a_val = E**2
x = symbols('x', real=True)
f = log((1/cos(x) + sin(x)/cos(x))/a_val)

# f(0) = -2 확인
f_at_0 = f.subs(x, 0)
print(f'f(0) = {f_at_0} = {float(f_at_0)}', flush=True)
assert abs(float(f_at_0) - (-2.0)) < 1e-10, f'Expected -2, got {float(f_at_0)}'

# f'(x) = sec(x) 확인
f_prime = diff(f, x)
f_prime_simplified = simplify(f_prime)
print(f'f\'(x) simplified = {f_prime_simplified}', flush=True)

# f'(0) = 1 확인
f_prime_at_0 = f_prime.subs(x, 0)
print(f'f\'(0) = {f_prime_at_0}', flush=True)
assert abs(float(f_prime_at_0) - 1.0) < 1e-10, f'Expected 1, got {float(f_prime_at_0)}'

# g'(-2) = 1/f'(0) = 1 확인
b_val = 1 / float(f_prime_at_0)
print(f'b = {b_val}', flush=True)
assert abs(b_val - 1.0) < 1e-10, f'Expected 1, got {b_val}'

# ab = e^2 확인
ab = float(a_val) * b_val
expected_ab = float(E**2)
print(f'ab = {ab}, e^2 = {expected_ab}', flush=True)
assert abs(ab - expected_ab) < 1e-10, f'Expected {expected_ab}, got {ab}'

print('VERIFY_PASS')