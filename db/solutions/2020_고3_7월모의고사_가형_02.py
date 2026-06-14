import sympy as sp
val = sp.tan(sp.Rational(4,3)*sp.pi)
expected = sp.sqrt(3)
if sp.simplify(val - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', val)