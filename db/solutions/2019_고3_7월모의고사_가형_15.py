"""
2019 고3 10월 모의고사 (원문제 15번, 4점) — 파라미터화

[문제 구조]
  tan α = -p/q  (3π/2 < α < 2π, 즉 α는 4사분면 각) 이고 0 ≤ x < π/2 일 때
  부등식  cos x ≤ sin(x+α) ≤ k·cos x
  를 만족시키는 x 에 대하여 tan x 의 최댓값과 최솟값의 합을 구하는 문제.

[수학적 전개 — solve()가 sympy로 그대로 재현한다]
  p,q>0 이고 4사분면이므로 r = sqrt(p²+q²) 일 때  sin α = -p/r, cos α = q/r.
  sin(x+α) = sin x·cos α + cos x·sin α = (q·sin x - p·cos x)/r

  좌변 부등식  cos x ≤ (q sin x - p cos x)/r
    ⇔ r cos x ≤ q sin x - p cos x  ⇔ (r+p) cos x ≤ q sin x  ⇔ tan x ≥ (r+p)/q  = tan_min

  우변 부등식  (q sin x - p cos x)/r ≤ k cos x
    ⇔ q sin x ≤ (p + k r) cos x  ⇔ tan x ≤ (p + k r)/q = tan_max

  [0, π/2) 에서 tan x 는 증가함수이므로 구간을 만족하는 tan x 의 최솟값·최댓값은
  각각 tan_min, tan_max 이고 답은 그 합 = (2p + r(1+k)) / q.
  (구간이 성립하려면 tan_min < tan_max ⇔ k > 1 이어야 한다.)

  원문제: p=5, q=12, k=2 → r=13 → 최솟값 3/2, 최댓값 31/12, 합 49/12 (= 선택지 ④).

[파라미터]
  p, q : tan α = -p/q 를 정의하는 분자·분모 (4사분면 각의 크기) — value(prm)에 직접 쓰임
  k    : 우변 부등식의 계수 sin(x+α) ≤ k·cos x — value(prm)에 직접 쓰임
  OPT  : 시험에 실제로 배치된 5지선다 보기 값(등차수열 31,37,43,49,55 /12)

  p, q, k 세 파라미터 모두 실제로 value(prm)를 바꾸고(아래에서 직접 검증), 그 결과
  choices(prm)와 비교했을 때 "가장 가까운 보기 번호"인 solve(prm)도 함께 바뀐다
  (예: p=5→10 이면 답은 ⑤, q=12→24 이면 답은 ③로 원문제 ④와 달라짐).
"""

import sympy as sp
from sympy import Rational, sqrt, sin, cos, symbols, simplify, N, Abs

CANDIDATE = 4  # ★원문제 정답: ④ (49/12) — 절대 바꾸지 않음

PARAMS = dict(
    p=5,   # tan α = -p/q 의 분자
    q=12,  # tan α = -p/q 의 분모
    k=2,   # 우변 부등식 계수: sin(x+α) ≤ k·cos x
    OPT=(Rational(31, 12), Rational(37, 12), Rational(43, 12), Rational(49, 12), Rational(55, 12)),
)


def value(prm):
    """tan x 의 최댓값과 최솟값의 합을 sympy 로 실제 계산한다."""
    p = sp.nsimplify(prm['p'])
    q = sp.nsimplify(prm['q'])
    k = sp.nsimplify(prm['k'])

    if p <= 0 or q <= 0:
        raise ValueError('p, q 는 양수여야 α가 4사분면 각으로 성립한다')
    if k <= 1:
        # tan_min = (r+p)/q >= (p + k r)/q = tan_max 가 되어 구간이 성립하지 않음
        raise ValueError('k <= 1 이면 부등식을 만족하는 구간이 존재하지 않는다')

    r = sqrt(p ** 2 + q ** 2)          # sin^2+cos^2=1, 4사분면 α → cosα=q/r, sinα=-p/r
    sin_a = -p / r
    cos_a = q / r

    x = symbols('x', real=True, positive=True)
    # sin(x+α) = sin x cos α + cos x sin α 를 실제로 전개
    sin_x_plus_a = sp.sin(x) * cos_a + sp.cos(x) * sin_a

    # 경계값 후보: 부등식이 등호로 성립할 때의 tan x
    #   cos x = sin(x+α)  ⇔  (r+p) cos x = q sin x  ⇔  tan x = (r+p)/q
    #   sin(x+α) = k cos x  ⇔  q sin x = (p+kr) cos x  ⇔  tan x = (p+kr)/q
    tan_min = (r + p) / q
    tan_max = (p + k * r) / q
    if simplify(tan_min - tan_max) >= 0:
        raise ValueError('tan_min >= tan_max — 구간이 성립하지 않는다')

    # sympy 로 경계에서 실제 등호가 성립하는지 검증 (수식 전개가 맞는지 확인)
    x_min = sp.atan(tan_min)
    x_max = sp.atan(tan_max)
    eq_left = simplify(sp.cos(x_min) - sin_x_plus_a.subs(x, x_min))
    eq_right = simplify(k * sp.cos(x_max) - sin_x_plus_a.subs(x, x_max))
    if eq_left != 0 or eq_right != 0:
        raise ValueError('경계 조건 검증 실패 — 수식 전개가 맞지 않는다')

    return simplify(tan_min + tan_max)


def choices(prm):
    """시험에 실제로 배치된 5지선다 보기(등차수열)."""
    opts = tuple(sp.nsimplify(o) for o in prm['OPT'])
    if len(opts) != 5:
        raise ValueError('보기는 5개여야 한다')
    return opts


def solve(prm):
    """value(prm)에 가장 가까운 보기의 번호(1~5)를 반환한다."""
    v = value(prm)
    opts = choices(prm)
    vN = N(v)
    diffs = [Abs(N(o) - vN) for o in opts]
    best = min(diffs)
    return diffs.index(best) + 1


def statement(prm):
    p, q, k = prm['p'], prm['q'], prm['k']
    opts = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts_str = ' '.join(f'{lab} {o}' for lab, o in zip(labels, opts))
    return (
        f"tan α = -{p}/{q} (3π/2 < α < 2π)이고 0 ≤ x < π/2일 때, "
        f"부등식 cos x ≤ sin(x+α) ≤ {k}cos x 를 만족시키는 x에 대하여 "
        f"tan x의 최댓값과 최솟값의 합은?\n{opts_str}"
    )


# 유도한 보기가 원문제 보기와 정확히 같은지 고정 검증
assert choices(PARAMS) == (Rational(31, 12), Rational(37, 12), Rational(43, 12), Rational(49, 12), Rational(55, 12))

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
