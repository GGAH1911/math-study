import sympy as sp
m = sp.Symbol('m', real=True)
eq = 7*m**2 - 8*m + 1
roots = sp.solve(eq, m)
assert len(roots) == 2
assert sp.Rational(1, 7) in roots and 1 in roots
p = 2*sp.sqrt(2)
q = sp.Rational(1, 7)
f_q = 4*abs(2*q - 1)
result = f_q / (p**2)
result_simplified = sp.simplify(result)
assert result_simplified == sp.Rational(5, 14), f'Expected 5/14, got {result_simplified}'
print('VERIFY_PASS')