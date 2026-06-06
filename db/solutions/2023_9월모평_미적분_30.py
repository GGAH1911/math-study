import sympy as sp
from sympy import symbols, integrate, simplify

# f'(x) = 4*x^2*(x+3)
# f(x) = x^4 + 4*x^3 + d
x = symbols('x', real=True)
d = symbols('d', real=True)

f_prime = 4*x**2*(x+3)
f = x**4 + 4*x**3 + d

# Check f(1) - f(0) and f(2) - f(0)
f_1_minus_f_0 = f.subs(x, 1) - f.subs(x, 0)
f_2_minus_f_0 = f.subs(x, 2) - f.subs(x, 0)

print(f'f(1) - f(0) = {f_1_minus_f_0}')
print(f'f(2) - f(0) = {f_2_minus_f_0}')

# Integral computation
integral_result = 1/f_1_minus_f_0 - 1/f_2_minus_f_0
integral_simplified = simplify(integral_result)

print(f'Integral result: {integral_simplified}')
print(f'As fraction: {sp.Rational(43, 240)}')

# Verify p + q
from math import gcd
gcd_val = gcd(43, 240)
print(f'gcd(43, 240) = {gcd_val}')
print(f'p + q = 240 + 43 = {240 + 43}')

if integral_simplified == sp.Rational(43, 240):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')