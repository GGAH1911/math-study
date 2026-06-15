"""2019 고3 7월모의고사 가형 26번 — 파라미터 솔버 (수동).
f 미분가능, f(1)=0, (xf'-f)/x² = x e^x.  좌변=(f/x)' → f/x=∫x e^x dx=(x-1)e^x+C.
f(1)=0 → C=0 → f(x)=x(x-1)e^x.  f(3)·f(-3)=6e³·12e^{-3}=72. (답 72)"""
import sympy as sp
def solve():
    x = sp.symbols('x'); C = sp.symbols('C')
    fx = x*((x-1)*sp.exp(x) + C)             # f = x·(∫x e^x dx)
    Cv = sp.solve(sp.Eq(fx.subs(x,1), 0), C)[0]
    f = fx.subs(C, Cv)
    return sp.simplify(f.subs(x,3)*f.subs(x,-3))
assert solve() == 72
print('VERIFY_PASS')
