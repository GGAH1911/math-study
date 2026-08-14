# f(x)=x^3-12x+k, [0,3] 에서 최댓값 40 → 최솟값?
# 임계점과 끝점에서의 값을 모두 구해 최댓값 조건으로 k 를 풀고, 그 k 로 최솟값을 구한다.
CANDIDATE = 24
import sympy as sp

x, k = sp.symbols('x k', real=True)
f = x**3 - 12*x + k
crit = [c for c in sp.solve(sp.diff(f, x), x) if c.is_real and 0 <= c <= 3]
pts = [sp.Integer(0), sp.Integer(3)] + list(crit)
vals = [sp.simplify(f.subs(x, p)) for p in pts]
k0 = sp.solve(sp.Eq(sp.Max(*vals), 40), k)[0]
mn = min(sp.simplify(v.subs(k, k0)) for v in vals)
print('VERIFY_PASS' if sp.simplify(mn - CANDIDATE) == 0 else 'VERIFY_FAIL')
