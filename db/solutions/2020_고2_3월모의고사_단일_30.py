import sympy as sp
# f(x)=√(ax-3)+2 (a>=3/2, x>=2). g(x)=min(f(x), f^{-1}(x)), f^{-1}(x)=((x-2)²+3)/a.
# h(n)=#(서로다른 y=g(x)∩y=x-n). h(1)=h(3)<h(2) → a=6. g(4)=q/p, p+q?
CANDIDATE = 13
x = sp.symbols('x', real=True)
a = 6
f = sp.sqrt(a*x - 3) + 2
finv = ((x - 2)**2 + 3)/a
def h(n):
    pts = set()
    for s in sp.solve(sp.Eq(f, x - n), x):              # g=f (f<=finv 영역)
        if s.is_real and s >= 2 and f.subs(x, s) <= finv.subs(x, s):
            pts.add(round(float(s), 6))
    for s in sp.solve(sp.Eq(finv, x - n), x):            # g=finv (접점=중근 1점)
        if s.is_real and s >= 2 and finv.subs(x, s) <= f.subs(x, s):
            pts.add(round(float(s), 6))
    return len(pts)
ok = (h(1) == h(3) < h(2))                              # a=6 검증 (2=2<3)
g4 = sp.Rational((4 - 2)**2 + 3, a)                      # f^{-1}(4)=7/6
print('VERIFY_PASS' if ok and g4.q + g4.p == CANDIDATE else 'VERIFY_FAIL')
