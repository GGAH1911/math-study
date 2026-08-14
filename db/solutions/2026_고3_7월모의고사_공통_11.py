# v(t)=3t^2-6t+k, x(t)=∫v. 보기 ㄱㄴㄷ 을 각각 실제로 계산해 참거짓을 판정한다.
import sympy as sp

t, k = sp.symbols('t k', real=True)
v = 3*t**2 - 6*t + k
x = sp.integrate(v, (t, 0, t))                       # 원점 출발 → 위치

def dist(kv, t0, t1):
    """구간에서 실제로 움직인 거리 = ∫|v| (부호 바뀌는 지점에서 쪼갠다)."""
    vv = v.subs(k, kv)
    pts = [r for r in sp.solve(vv, t) if r.is_real and t0 < r < t1]
    edges = [t0] + sorted(pts) + [t1]
    return sum(sp.Abs(sp.integrate(vv, (t, edges[i], edges[i+1]))) for i in range(len(edges)-1))

g = sp.simplify(x.subs(k, 0).subs(t, 1) + 2) == 0                       # ㄱ: 위치가 -2
n = sp.simplify(dist(2, 0, 3) - sp.Abs(x.subs(k, 2).subs(t, 3))) == 0   # ㄴ: 거리 = 변화량
d = sp.simplify(dist(-9, 0, 4) - 34) == 0                              # ㄷ: 거리 34
truth = {'ㄱ': bool(g), 'ㄴ': bool(n), 'ㄷ': bool(d)}
choices = {1: {'ㄱ'}, 2: {'ㄱ', 'ㄴ'}, 3: {'ㄱ', 'ㄷ'}, 4: {'ㄴ', 'ㄷ'}, 5: {'ㄱ', 'ㄴ', 'ㄷ'}}
true_set = {kk for kk, vv in truth.items() if vv}
pick = [kk for kk, vv in choices.items() if vv == true_set]
print('VERIFY_PASS' if pick == [3] else 'VERIFY_FAIL')
