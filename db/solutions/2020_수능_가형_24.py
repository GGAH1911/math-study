import sympy as sp

# 2020 수능 가형 24: P(t,sin t) 중심, x축 접하는 원 C (반지름 sin t). 접점 Q=(t,0).
# R = 선분 OP 와 C 의 교점. lim_{t→0+} OQ/OR = a+b√2, a+b?  (정답 2)
# OQ=t.  OR=|OP|-반지름=√(t²+sin²t)-sin t.
CANDIDATE = 2
t = sp.symbols('t', positive=True)
OQ = t
OR = sp.sqrt(t**2 + sp.sin(t)**2) - sp.sin(t)
L = sp.nsimplify(sp.limit(OQ / OR, t, 0, '+'))     # = 1 + √2
b = L.coeff(sp.sqrt(2))                             # 1
a = sp.simplify(L - b * sp.sqrt(2))                 # 1
print('VERIFY_PASS' if a + b == CANDIDATE else 'VERIFY_FAIL')
