import sympy as sp
# 등비 a2=6, a5=48. a6?
CANDIDATE = 96
a1, r = sp.symbols('a1 r', positive=True)
sol = sp.solve([a1*r - 6, a1*r**4 - 48], [a1, r])[0]
a1v, rv = sol
print('VERIFY_PASS' if a1v*rv**5 == CANDIDATE else 'VERIFY_FAIL')
