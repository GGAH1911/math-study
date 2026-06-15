import sympy as sp
import numpy as np
# f(x)=3x²+tx (x<0), -3x²+tx (x>=0). t>=6-3√2. g(t)=min k 만족:
# (가) [k-1,k]서 f 최대 x=k, (나) [k,k+1]서 f 최소 x=k+1. 3∫₂⁴ (6g(t)-3)² dt ?
CANDIDATE = 37
def f(x, tv):
    return 3*x*x + tv*x if x < 0 else -3*x*x + tv*x
def g(tv):                                   # 유도된 g(t)
    return 0.5 - (6*tv-9)**0.5/6 if tv < 3 else (tv-3)/6
# 검증: 표본 t에서 g(t)가 (가)(나) 만족 & 최소(아래로 0.05 내리면 무효)
ok = True
for tv in [2.2, 2.5, 2.9, 3.0, 3.5, 4.0]:
    k = g(tv)
    def conds(kk):
        x1 = np.linspace(kk-1, kk, 400); x2 = np.linspace(kk, kk+1, 400)
        ga = all(f(x, tv) <= f(kk, tv) + 1e-6 for x in x1)
        na = all(f(x, tv) >= f(kk+1, tv) - 1e-6 for x in x2)
        return ga and na
    if not (conds(k) and not conds(k - 0.05)):
        ok = False
# 적분: (6g(t)-3)² 를 g(t) 식에서 직접 구성
t = sp.symbols('t', positive=True)
glo = sp.Rational(1, 2) - sp.sqrt(6*t-9)/6   # t<3
ghi = (t-3)/6                                 # t>=3
I = sp.integrate((6*glo-3)**2, (t, 2, 3)) + sp.integrate((6*ghi-3)**2, (t, 3, 4))
print('VERIFY_PASS' if ok and 3*I == CANDIDATE else 'VERIFY_FAIL')
