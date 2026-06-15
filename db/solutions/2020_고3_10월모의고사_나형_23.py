import sympy as sp
# X~B(n,1/2), V(2X+1)=15. n?  V(2X+1)=4·n/4=n
CANDIDATE = 15
n = sp.symbols('n', positive=True)
nv = sp.solve(4*(n*sp.Rational(1,4)) - 15, n)[0]
print('VERIFY_PASS' if nv == CANDIDATE else 'VERIFY_FAIL')
