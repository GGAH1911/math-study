from sympy import symbols, solve, ln, Abs
import numpy as np

x = symbols('x', real=True)

# f(x) = x^3 + (1/3)x^2 + (1/3)x
def f_val(x_val):
    return x_val**3 + (1/3)*x_val**2 + (1/3)*x_val

def f_prime(x_val):
    return 3*x_val**2 + (2/3)*x_val + (1/3)

# Verify condition (나): 4*g'(f(1)) = 3*f(1) - 4
f_1 = f_val(1)
g_prime_f1 = 1 / f_prime(1)  # g'(f(1)) = 1/f'(g(f(1))) = 1/f'(1)

lhs = 4 * g_prime_f1
rhs = 3 * f_1 - 4

if abs(lhs - rhs) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {lhs} != {rhs}')