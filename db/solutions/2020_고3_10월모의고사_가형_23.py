import sympy as sp
# X~B(n,1/3), V(X)=200. E(X)?  V=2n/9=200→n=900, E=n/3
CANDIDATE = 300
n = sp.symbols('n', positive=True)
nv = sp.solve(n*sp.Rational(1,3)*sp.Rational(2,3) - 200, n)[0]
print('VERIFY_PASS' if nv*sp.Rational(1,3) == CANDIDATE else 'VERIFY_FAIL')
