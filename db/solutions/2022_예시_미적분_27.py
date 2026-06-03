import sympy as sp
x = sp.Symbol('x')
f = x * sp.ln(x**2 + 1)
area = sp.integrate(f, (x, 0, 1))
expected = sp.ln(2) - sp.Rational(1, 2)
if sp.simplify(area - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Computed: {sp.simplify(area)}, Expected: {expected}')