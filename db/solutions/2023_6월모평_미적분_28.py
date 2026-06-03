import sympy as sp
x = sp.Symbol('x', real=True)
b, c = -6, 10
f = sp.Rational(1,2)*(x-1)*(x**2 + b*x + c)
fp = sp.diff(f, x)
fpp = sp.diff(fp, x)
# 최고차항 계수 1/2
assert sp.Poly(f, x).LC() == sp.Rational(1,2)
# 실근이 x=1 뿐
real_roots = [r for r in sp.solve(f, x) if r.is_real]
assert real_roots == [1]
assert b**2 - 4*c < 0  # x^2+bx+c 실근 없음
# f'(2)=0
assert fp.subs(x, 2) == 0
# f(2)=1, g(2)=0
f2 = f.subs(x, 2)
assert f2 == 1
# g''(2) < 0 (g 극대)
assert fpp.subs(x, 2)/f2 < 0
# (다): |f(x)|=1 서로 다른 실근 3개
sols = set()
for eq in [f-1, f+1]:
    for r in sp.solve(eq, x):
        if r.is_real:
            sols.add(sp.nsimplify(r))
assert len(sols) == 3, sols
# g의 극소: 또 다른 임계점 x=8/3
crit = set(sp.solve(fp, x))
assert crit == {2, sp.Rational(8,3)}
x0 = sp.Rational(8,3)
g_min = sp.log(sp.Abs(f.subs(x, x0)))
target = sp.log(sp.Rational(25, 27))
assert sp.simplify(g_min - target) == 0
print('VERIFY_PASS')