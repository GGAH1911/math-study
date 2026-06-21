import sympy as sp
val = sp.log(54, 3) + sp.log(sp.Rational(1,36), 9)
val = sp.nsimplify(sp.simplify(val))
print('VERIFY_PASS' if sp.simplify(val - 2) == 0 else 'VERIFY_FAIL')