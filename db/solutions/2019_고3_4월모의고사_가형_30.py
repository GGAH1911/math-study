"""2019 고3 4월모의고사 가형 30번 — 파라미터 솔버 (수동 작성).
문제: f(x)=x³+ax²+bx (a,b 정수). g(x)=e^{f(x)}-f(x) 가 x=α,-1,β (α<-1<β) 에서만 극값.
      y=|g(x)-g(α)| 가 미분불가능한 점이 정확히 2개일 때 (f(-1))² 의 최댓값. (답 9)
구조: g=G(f), G(t)=e^t-t (t=0서 최소). sign g'(x)=sign f'(x)·sign f(x) (오버플로 없이 극값 판정).
      g의 극값 = (f'=0 ∧ f≠0) ∪ (f 의 단순근). '미분불가 점' = g(x)=g(α) 를 횡단(g'≠0)하는 점 수.
      정수 (a,b) 탐색: 극값={α,-1,β} 이고 미분불가=2 인 것 → (5,7):f(-1)=-3, (4,5):f(-1)=-2.
      max (f(-1))² = (-3)² = 9  (at a=5,b=7: f=x(x²+5x+7), 실근 x=0뿐, f'근 -1,-7/3 → 극값 {-7/3,-1,0}).
재생산: 정수격자 (a,b) 탐색 — 조건 만족 해를 모두 생성.
"""
import numpy as np


def fx(x, a, b):
    return x ** 3 + a * x * x + b * x


def fpx(x, a, b):
    return 3 * x * x + 2 * a * x + b


def analyze(a, b):
    cand = np.concatenate([np.roots([3, 2 * a, b]), np.roots([1, a, b, 0])])
    cand = sorted({round(float(r.real), 9) for r in cand if abs(r.imag) < 1e-9})

    def sg(x):                                   # sign g' = sign f' · sign f
        p, q = fpx(x, a, b), fx(x, a, b)
        sp = 0 if abs(p) < 1e-12 else np.sign(p)
        sq = 0 if abs(q) < 1e-12 else np.sign(q)
        return sp * sq

    ext = sorted({round(c, 6) for c in cand
                  if sg(c - 1e-5) and sg(c + 1e-5) and sg(c - 1e-5) != sg(c + 1e-5)})
    if not (len(ext) == 3 and abs(ext[1] + 1) < 1e-6 and ext[0] < -1 < ext[2]):
        return None
    alpha = ext[0]
    fa = fx(alpha, a, b)
    ga = np.exp(np.clip(fa, -50, 50)) - fa
    xs = np.linspace(min(cand) - 6, max(cand) + 6, 400000)   # |g-g(α)| 횡단 영점 수
    g = np.exp(np.clip(fx(xs, a, b), -50, 50)) - fx(xs, a, b)
    s = np.sign(g - ga)
    nd = 0
    for i in np.where(s[:-1] * s[1:] < 0)[0]:
        xm = xs[i]
        if abs(fpx(xm, a, b)) > 1e-6 and abs(fx(xm, a, b)) > 1e-6:   # g'≠0 (횡단)
            nd += 1
    return nd, (-1) ** 3 + a * (-1) ** 2 + b * (-1)


def solve(rng=15):
    best = -1
    for a in range(-rng, rng + 1):
        for b in range(-rng, rng + 1):
            r = analyze(a, b)
            if r and r[0] == 2:
                best = max(best, r[1] ** 2)
    return best


CANDIDATE = 9
assert solve() == CANDIDATE, solve()
print('VERIFY_PASS')
