import sympy as sp
# 2cos²θ-sin²θ=1. 60sin²θ?  (cos²=1-sin² → sin²=1/3)
CANDIDATE = 20
s2 = sp.symbols('s2')   # sin²θ
v = sp.solve(sp.Eq(2*(1-s2)-s2, 1), s2)[0]
print('VERIFY_PASS' if 60*v == CANDIDATE else 'VERIFY_FAIL')
