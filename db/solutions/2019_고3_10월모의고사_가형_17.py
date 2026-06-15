import sympy as sp
import numpy as np
from sympy import exp, symbols, diff, solve

x = symbols('x', real=True)
a, b = 3, 2*sp.E

# x > 0에서의 함수
f_pos = a*x*exp(2*x) + b*x**2

# f(1/2) = 2e 검증
f_half = f_pos.subs(x, sp.Rational(1,2))
print(f'f(1/2) = {f_half}')
print(f'Expected: 2e = {2*sp.E}')
assert f_half == 2*sp.E, 'f(1/2) check failed'

# x < 0에서 f(x) = 3x이므로 f'(x) = 3
f_neg = 3*x
f_prime_neg = diff(f_neg, x)

# x > 0에서의 도함수
f_prime_pos = diff(f_pos, x)
f_prime_half = f_prime_pos.subs(x, sp.Rational(1,2))
print(f'f\'(1/2) = {f_prime_half}')
print(f'Expected: 8e = {8*sp.E}')
assert f_prime_half == 8*sp.E, 'f\'(1/2) check failed'

# x=0에서 미분가능성 검증
f_prime_at_0_pos = f_prime_pos.subs(x, 0)
f_prime_at_0_neg = 3
print(f'f\'(0+) = {f_prime_at_0_pos}, f\'(0-) = {f_prime_at_0_neg}')
assert f_prime_at_0_pos == f_prime_at_0_neg, 'Differentiability check failed'

print('VERIFY_PASS')