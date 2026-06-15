import sympy as sp
# X~B(36,2/3). E(2X-a)=V(2X-a). a?  E=24,V=8; 48-a=32
CANDIDATE = 16
a = sp.symbols('a')
E, V = 36*sp.Rational(2,3), 36*sp.Rational(2,3)*sp.Rational(1,3)
av = sp.solve(sp.Eq(2*E - a, 4*V), a)[0]
print('VERIFY_PASS' if av == CANDIDATE else 'VERIFY_FAIL')
