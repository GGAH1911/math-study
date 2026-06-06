"""2021학년도 9월모평 나형 13번 — 검증기 (수동 작성).
문제: 수직선 위 점 P의 속도 v(t)=t²-at (a>0). t=0부터 '움직이는 방향이 바뀔 때까지'
      움직인 거리가 9/2. 상수 a? (답 ③ 3)
검증: 답 a=3 을 원래 속도식에 역대입 → 방향전환 시각(=a)까지의 이동거리 ∫|v|dt 가 9/2 인지 확인.
      (정적분의 활용: v<0 구간이라 이동거리=∫(-v)dt. a³/6=9/2 ⇔ a=3.)
"""
import sympy as sp

t = sp.symbols('t', real=True, nonnegative=True)
a = sp.Integer(3)                     # 답 ③ 역대입
v = t**2 - a * t                      # 원래 속도식 (이미지: v(t)=t²-at, a>0)

# 출발(t=0) 이후 속도 부호가 처음 바뀌는 시각 = 움직이는 방향이 바뀌는 시각
pos_roots = sorted(r for r in sp.solve(sp.Eq(v, 0), t) if r > 0)
assert pos_roots, "양의 방향전환 시각이 없음"
T = pos_roots[0]                      # = a = 3

# 0<t<T 에서 v<0 (음의 방향)임을 확인 → 이동거리 = ∫₀ᵀ |v| dt = ∫₀ᵀ (-v) dt
assert v.subs(t, T / 2) < 0, "방향전환 전 구간에서 v<0 이 아님"
dist = sp.integrate(-v, (t, 0, T))

print('VERIFY_PASS' if sp.simplify(dist - sp.Rational(9, 2)) == 0 else 'VERIFY_FAIL')
