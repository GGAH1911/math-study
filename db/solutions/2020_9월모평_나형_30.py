import sympy as sp

# 2020 9월모평 나형 30: 최고차계수 1인 사차함수 f. f(-1),f(0),f(1),f(2)가 등차수열.
# (-1,f(-1)) 접선과 (2,f(2)) 접선이 (k,0)에서 만남. f(2k)=20 → f(4k)?
CANDIDATE = 42
x, a, b, c, d, k = sp.symbols('x a b c d k')
f = x**4 + a * x**3 + b * x**2 + c * x + d
fm1, f0, f1, f2 = [f.subs(x, t) for t in (-1, 0, 1, 2)]
# 등차수열: 연속한 차가 동일
ab = sp.solve([sp.Eq(f0 - fm1, f1 - f0), sp.Eq(f1 - f0, f2 - f1)], [a, b], dict=True)[0]
f = f.subs(ab)                       # a=-2, b=-1
fp = sp.diff(f, x)
# 접선 at x=-1, x=2 가 점 (k,0) 통과
eqA = sp.Eq(f.subs(x, -1) + fp.subs(x, -1) * (k - (-1)), 0)
eqB = sp.Eq(f.subs(x, 2) + fp.subs(x, 2) * (k - 2), 0)
eqF = sp.Eq(f.subs(x, 2 * k), 20)    # f(2k)=20
sols = sp.solve([eqA, eqB, eqF], [c, d, k], dict=True)
vals = set()
for s in sols:
    if s[k].is_real:
        vals.add(sp.simplify(f.subs(s).subs(x, 4 * s[k])))
print('VERIFY_PASS' if CANDIDATE in vals else 'VERIFY_FAIL')
