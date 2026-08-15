"""2019 고3 4월모의고사 나형 23번 — 파라미터화 솔버.

원문제: 실수 x에 대한 두 조건
  p: -5 ≤ x ≤ 10
  q: -6 ≤ x ≤ a
에서 p가 q이기 위한 충분조건이 되도록(즉 p ⇒ q) 하는 실수 a의 최솟값을 구하시오. (답 10)

수학 구조:
  p ⇒ q  ⟺  {x : p} ⊆ {x : q}  ⟺  [p_lo, p_hi] ⊆ [q_lo, a]
  ⟺  (q_lo ≤ p_lo)  그리고  (a ≥ p_hi)
  ⟹  a의 최솟값 = p_hi

파라미터화 포인트:
  - p 구간을 "중심 p_center · 반지름 p_halfwidth" 로 표현한다.
    p_lo = p_center - p_halfwidth,  p_hi = p_center + p_halfwidth
    답(a의 최솟값) = p_hi = p_center + p_halfwidth 이므로
    p_center, p_halfwidth 두 값을 각각 바꾸면 답이 실제로 달라진다(살아있는 파라미터 2개).
  - q_lo 는 "q_lo ≤ p_lo" 라는 성립 조건(문제가 유효하려면 반드시 필요한 부등식)을 결정한다.
    답의 값 자체에는 영향을 주지 않지만, 조건이 깨지면 문제 자체가 성립하지 않으므로 예외를 던진다.
"""

import sympy as sp


def solve(prm):
    p_center = sp.nsimplify(prm['p_center'])
    p_halfwidth = sp.nsimplify(prm['p_halfwidth'])
    q_lo = sp.nsimplify(prm['q_lo'])

    p_lo = p_center - p_halfwidth
    p_hi = p_center + p_halfwidth

    # p ⇒ q 가 성립하려면(=p가 q의 부분조건이려면) 먼저 q_lo ≤ p_lo 이어야 한다.
    # 이게 깨지면 아무리 a를 키워도 [p_lo,p_hi]가 [q_lo,a]에 못 들어가므로 문제가 성립하지 않는다.
    if not bool(q_lo <= p_lo):
        raise ValueError('q_lo ≤ p_lo 조건이 성립하지 않아 p가 q의 충분조건이 될 수 없음')

    # a에 대한 부등식 a ≥ p_hi 를 sympy로 실제로 풀어 그 최솟값(하한)을 답으로 취한다.
    a = sp.symbols('a', real=True)
    region = sp.solve_univariate_inequality(a >= p_hi, a, relational=False)
    a_min = region.inf
    return a_min


def statement(prm):
    p_center = sp.nsimplify(prm['p_center'])
    p_halfwidth = sp.nsimplify(prm['p_halfwidth'])
    q_lo = sp.nsimplify(prm['q_lo'])
    p_lo = p_center - p_halfwidth
    p_hi = p_center + p_halfwidth

    def fmt(x):
        x = sp.nsimplify(x)
        return str(x) if x.is_Integer else sp.nsimplify(x)

    return (
        f"실수 x에 대하여 두 조건 p, q가\n"
        f"  p: {fmt(p_lo)} \\le x \\le {fmt(p_hi)},\n"
        f"  q: {fmt(q_lo)} \\le x \\le a\n"
        f"일 때, p가 q이기 위한 충분조건이 되도록 하는 실수 a의 최솟값을 구하시오."
    )


# p_center=5/2, p_halfwidth=15/2 → p_lo=-5, p_hi=10 (원문제와 동일)
PARAMS = dict(p_center=sp.Rational(5, 2), p_halfwidth=sp.Rational(15, 2), q_lo=-6)

CANDIDATE = 10

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
