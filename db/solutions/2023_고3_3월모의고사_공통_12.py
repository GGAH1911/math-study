import sympy as sp
t = sp.Symbol('t', positive=True)
c = (2*t**2 - 1)/4
AB_squared = 2*(1 + 4*c)
AB = sp.sqrt(AB_squared)
assert sp.simplify(AB - 2*t) == 0, 'Constraint |AB| = 2t not satisfied'
result = sp.limit(c/t**2, t, sp.oo)
assert result == sp.Rational(1,2), f'Limit should be 1/2, got {result}'
print('VERIFY_PASS')