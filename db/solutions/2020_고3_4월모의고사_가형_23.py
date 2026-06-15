import sympy as sp
# 등차 a1=6, a3+a6=a11. a4?
CANDIDATE = 12
d = sp.symbols('d')
a = lambda n: 6 + (n-1)*d
dv = sp.solve(sp.Eq(a(3)+a(6), a(11)), d)[0]
print('VERIFY_PASS' if a(4).subs(d, dv) == CANDIDATE else 'VERIFY_FAIL')
