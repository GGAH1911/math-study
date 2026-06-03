import sympy as sp
import numpy as np
from sympy import exp, ln, symbols, solve, diff

x = symbols('x', real=True)
f = exp(2*x) + exp(x) - 1
f_prime = diff(f, x)

f_at_0 = f.subs(x, 0)
f_prime_at_0 = f_prime.subs(x, 0)

a = symbols('a', real=True)
eq = exp(2*a) + exp(a) - 1 - 5
a_val = solve(eq, a)
a_val = [val for val in a_val if val.is_real and val > -float('inf')][0]

f_prime_at_a = f_prime.subs(x, a_val)

h_prime_at_0 = (5 * f_prime_at_0) / f_prime_at_a
result = float(h_prime_at_0)

if abs(result - 1.5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')