"""2019 고3 4월모의고사 나형 30번 — 파라미터 솔버 (수동 작성).
문제: f(x)=ax+b, g(x)=1/(ax+b-2)+3. (가) x>0서 1<g<3. (나) y=f 와 y=1/(x-2)+3 의 교점이
      제4사분면(x>0,y<0)에 없음. R={(a,b)} 에서 a²+b²의 최댓값 M. 100M. (a≠0) (답 306)
구조: (가) ⟺ a<0, b≤3/2 (x→0+서 ax+b→b<3/2 필요, a<0이면 x>0서 감소).
      쌍곡선 y=1/(x-2)+3 은 y=0 을 x=5/3(>0)서 지남 — Q4 진입 경계 코너.
      최댓점: 절편 최대 b=3/2 이고 직선이 (5/3,0) 통과 → a·(5/3)+b=0 → a=-3b/5=-9/10.
      M = a²+b² = 81/100 + 9/4 = 306/100 = 3.06 → 100M = 306.
재생산: 쌍곡선 상수(asymptote·shift) 파라미터화.
"""
import numpy as np
from fractions import Fraction as Fr

b = Fr(3, 2)                       # (가): 절편 최대
a = -Fr(3, 5) * b                  # 직선이 (5/3,0) 통과: a*(5/3)+b=0
M = a * a + b * b                  # = 3.06


def feasible(a, b):
    if a >= 0 or b > 1.5 + 1e-12:
        return False
    xs = np.linspace(1e-4, 500, 800)            # (가) x>0서 1<g<3
    g = 1 / (a * xs + b - 2) + 3
    if not np.all((g > 1) & (g < 3)):
        return False
    A, B, C = a, b - 2 * a - 3, 5 - 2 * b        # 교점 ax²+Bx+C=0
    disc = B * B - 4 * A * C
    if disc >= 0 and abs(A) > 1e-15:
        for x in [(-B + np.sqrt(disc)) / (2 * A), (-B - np.sqrt(disc)) / (2 * A)]:
            if abs(x - 2) < 1e-9:
                continue
            if x > 1e-9 and a * x + b < -1e-9:   # 교점이 Q4
                return False
    return True


# 수치 검증: feasible 영역에서 M 을 넘는 점이 없음 (해석적 최적이 진짜 최대)
mx = 0.0
for aa in np.linspace(-3, -1e-3, 300):
    for bb in np.linspace(-3, 1.5, 300):
        if feasible(aa, bb):
            mx = max(mx, aa * aa + bb * bb)
assert abs(float(M) - 3.06) < 1e-12, float(M)
assert mx <= float(M) + 2e-2, (mx, float(M))    # 그리드 해상도 오차 허용

CANDIDATE = 306
assert round(100 * float(M)) == CANDIDATE
print('VERIFY_PASS')
