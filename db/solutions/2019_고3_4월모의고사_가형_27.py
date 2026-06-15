"""2019 고3 4월모의고사 가형 27번 — 파라미터 솔버 (수동 작성).
문제: 미분가능 f,g, g=f⁻¹, g(2)=1, g(5)=5. ∫₁⁵ 40/(g'(f(x))·{f(x)}²) dx. (답 12)
구조: g=f⁻¹ → g(f(x))=x → g'(f(x))·f'(x)=1 → 1/g'(f(x))=f'(x).
      적분 = ∫₁⁵ 40 f'(x)/f(x)² dx = 40[-1/f(x)]₁⁵ = 40(1/f(1) - 1/f(5)).
      g(2)=1 → f(1)=2,  g(5)=5 → f(5)=5.  → 40(1/2 - 1/5) = 40·(3/10) = 12.
재생산: (g 의 두 점, 상수 40) 파라미터화.
"""
import sympy as sp


def solve(f_lo, f_hi, const=40):
    # f(lower)=f_lo, f(upper)=f_hi 에서 const(1/f_lo - 1/f_hi)
    return const * (sp.Rational(1, f_lo) - sp.Rational(1, f_hi))


# g(2)=1→f(1)=2 (하한), g(5)=5→f(5)=5 (상한)
CANDIDATE = 12
assert solve(2, 5) == CANDIDATE, solve(2, 5)
print('VERIFY_PASS')
