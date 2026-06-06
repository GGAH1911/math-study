import sympy as sp
x = sp.Symbol('x')
f = 4*x - 1
F = 2*x**2 - x + 1
g = 2*x + 1
G = x**2 + x
integral_f = sp.integrate(f, (x, 1, x))
check_a = sp.simplify(integral_f - (x*f - 2*x**2 - 1)) == 0
check_b = sp.expand(f*G + F*g - (8*x**3 + 3*x**2 + 1)) == 0
result = sp.integrate(g, (x, 1, 3))
if check_a and check_b and result == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')