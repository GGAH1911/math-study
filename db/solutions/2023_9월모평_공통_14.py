import sympy as sp
from sympy import symbols, integrate, Abs, simplify

x, t, a = symbols('x t a', real=True)
f = x * (x - 1) * (x - a)

# Test with a = -3 (satisfies a < -5/2 for condition 다)
a_val = -3
f_subs = f.subs(a, a_val)

# g(t) = integral from t to t+1 of f - integral from 0 to 1 of |f|
C = integrate(Abs(f_subs), (x, 0, 1))
g_neg1 = integrate(f_subs, (x, -1, 0)) - C
g_0 = integrate(f_subs, (x, 0, 1)) - C

# Check conditions
print('For a = -3:')
print(f'g(-1) = {float(g_neg1)} > 1: {float(g_neg1) > 1}')
print(f'g(0) = {float(g_0)} < -1: {float(g_0) < -1}')

# Verify f(-3) = 0
verify_root = f_subs.subs(x, -3)
print(f'\nf(-3) = {verify_root} (should be 0)')

if float(g_neg1) > 1 and float(g_0) < -1 and verify_root == 0:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')