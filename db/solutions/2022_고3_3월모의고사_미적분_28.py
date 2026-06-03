import sympy as sp
a = sp.Rational(3, 2)
# A_{2n} = (n*a, (n-1)*(a+1))
# limit of |A1 A_{2n}| / n as n->inf
# = sqrt(a^2 + (a+1)^2)
limit_val = sp.sqrt(a**2 + (a+1)**2)
expected = sp.sqrt(34) / 2
if sp.simplify(limit_val - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
