import sympy as sp
import numpy as np

# 2020 6월모평 나형 30 (킬러): 최고차계수 1, f(2)=3 인 삼차 f. g(x)=(ax-9)/(x-1) (x<1), f(x) (x>=1).
# y=g(x) 와 y=t 가 서로 다른 두 점에서만 만나는 t 의 집합 = {t=-1 또는 t>=3}. (g∘g)(-1)?
# 구조: f(2)=3 은 극대, 극소값 -1 → f'=3(x-2)(x-β), f(β)=-1 로 β, 상수항 결정.
CANDIDATE = 19

X, beta, r = sp.symbols('X beta r', real=True)
f_sym = X**3 - sp.Rational(3, 2) * (2 + beta) * X**2 + 6 * beta * X + r   # ∫3(x-2)(x-β)dx
sol = sp.solve([f_sym.subs(X, 2) - 3, f_sym.subs(X, beta) + 1], [beta, r], dict=True)
pick = [s for s in sol if s[beta].is_real and s[beta] > 2][0]
B, R = pick[beta], pick[r]
co = [float(c) for c in sp.Poly(f_sym.subs({beta: B, r: R}), X).all_coeffs()]   # [1,-9,24,-17]
def f(v):
    return ((co[0] * v + co[1]) * v + co[2]) * v + co[3]

a = 3   # 좌측가지 (ax-9)/(x-1) 의 x<1 치역=(a,∞), 조건의 t>=3 경계 ⟹ a=3

def count(t):
    n = 0
    if a != t:                       # 좌측: (a x-9)/(x-1)=t → x=(9-t)/(a-t), x<1 이면 1점
        if (9 - t) / (a - t) < 1:
            n += 1
    c = co[:]; c[-1] -= t            # f(x)=t, x>=1 인 서로 다른 실근 수 (중근=1점)
    rs = sorted(rt.real for rt in np.roots(c)
                if abs(rt.imag) < 1e-7 and rt.real >= 1 - 1e-9)
    distinct = [v for i, v in enumerate(rs) if i == 0 or v - rs[i - 1] > 1e-6]
    return n + len(distinct)

# 조건 검증: 교점 2개 ⟺ (t=-1 또는 t>=3)
ok = True
for t in [-3, -2, -1.0, -0.5, 0, 1, 2, 2.9, 3.0, 3.5, 5, 12]:
    want = abs(t + 1) < 1e-9 or t >= 3 - 1e-9
    if (count(t) == 2) != want:
        ok = False

def g(v):
    return (a * v - 9) / (v - 1) if v < 1 else f(v)

gg = g(g(-1.0))                      # g(-1)=6, g(6)=f(6)=19
print('VERIFY_PASS' if ok and abs(gg - CANDIDATE) < 1e-6 else 'VERIFY_FAIL')
