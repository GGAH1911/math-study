import sympy as sp
n = sp.symbols('n', positive=True)
numer = sp.Rational(5,1)/n + sp.Rational(3,1)/n**2
denom = sp.Rational(1,1)/n - sp.Rational(2,1)/n**3
expr = numer/denom
limit_val = sp.limit(expr, n, sp.oo)
candidate = 5
if sp.simplify(limit_val - candidate) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
