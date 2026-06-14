import sympy as sp
val = sp.sin(sp.pi/4) + sp.cos(sp.Rational(3,4)*sp.pi)
val = sp.simplify(val)
print('VERIFY_PASS' if val == 0 else 'VERIFY_FAIL')