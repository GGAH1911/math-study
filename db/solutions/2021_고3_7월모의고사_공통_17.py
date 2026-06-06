import sympy as sp
x = sp.Symbol('x')
f_prime = 3*x**2 + 6*x - 4
f = sp.integrate(f_prime, x) + 5  # +C where C=5 from f(1)=5 constraint
f_simplified = x**3 + 3*x**2 - 4*x + 5
assert sp.simplify(f - f_simplified) == 0, 'f(x) form incorrect'
assert f_simplified.subs(x, 1) == 5, 'f(1) constraint failed'
result = f_simplified.subs(x, 2)
if result == 17:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')