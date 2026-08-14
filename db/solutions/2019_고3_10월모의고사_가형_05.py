from sympy import symbols, Eq, sqrt, Rational, nsimplify, Abs
from sympy import solve as sp_solve

# ── 문제 구조 ──────────────────────────────────────────────────────────────
# 직선 y = (p/q)x 가 쌍곡선 x^2/k - y^2/b2 = 1 의 한 점근선일 때 주축의 길이 2a 를 구한다.
#   점근선 기울기 = sqrt(b2/k)  ⇒  sqrt(b2/k) = p/q 를 k 에 대해 실제로 sympy 로 푼다.
#   a = sqrt(k),  주축의 길이 = 2a.
#
# 파라미터(문제를 정하는 값):
#   b2 : 쌍곡선 y^2 항의 분모(원문제 64)               ← 값을 바꾸면 실제로 답(보기 번호)이 바뀐다
#   p, q : 점근선 기울기 p/q(원문제 1/2)                ← 값을 바꾸면 실제로 답(보기 번호)이 바뀐다
#   OPT : 객관식 보기 값 목록(원문제 30,32,34,36,38)
#
# 객관식이므로 value(수학적 답) 과 choices(보기 목록)를 분리하고, solve 는 "계산된 값에
# 가장 가까운 보기의 번호"를 돌려준다. 원문제는 계산값이 보기 중 하나와 정확히 일치하지만,
# 파라미터를 바꾸면 계산값이 달라져 가장 가까운 보기(=학생이 답으로 고를 보기)의 번호 자체가
# 달라진다 — 이것이 "실제로 답이 바뀌는" 지점이다.

CANDIDATE = 2  # 원문제 정답 = ②

PARAMS = dict(
    b2=64,                    # 쌍곡선: x^2/k - y^2/b2 = 1
    p=1, q=2,                 # 점근선 기울기 = p/q = 1/2
    OPT=(30, 32, 34, 36, 38), # 보기 값(①~⑤)
)


def value(prm):
    """주축의 길이 2a 를 sympy 로 실제로 계산한다."""
    b2 = Rational(prm['b2'])
    p = Rational(prm['p'])
    q = Rational(prm['q'])
    if p == 0:
        raise ValueError('점근선 기울기의 분모(q/p 구조)가 정의되지 않음: p=0')
    slope = p / q
    if slope <= 0:
        raise ValueError('기울기가 양수가 아니어서 이 쌍곡선 형태로 성립하지 않음')

    k = symbols('k', positive=True)
    eq = Eq(sqrt(b2 / k), slope)   # 점근선 조건: sqrt(b2/k) = slope
    sols = sp_solve(eq, k)
    if not sols:
        raise ValueError('주어진 조건을 만족하는 k(>0)가 존재하지 않음')
    kv = sols[0]
    if not kv.is_positive:
        raise ValueError('k가 양수 조건을 만족하지 않음')

    a = sqrt(kv)          # a^2 = k
    return 2 * a          # 주축의 길이


def choices(prm):
    """보기 목록(값에서 유도가 아니라 원문제 자체가 제시한 보기값 파라미터)."""
    opts = tuple(prm['OPT'])
    if len(opts) != 5:
        raise ValueError('보기는 5개여야 함')
    return opts


# 유도한 보기가 원문제 보기와 같은지 고정
assert choices(PARAMS) == (30, 32, 34, 36, 38)


def solve(prm):
    """계산된 값에 가장 가까운 보기의 번호(1~5)를 반환한다."""
    v = value(prm)
    opts = choices(prm)
    vN = v.evalf()
    diffs = [Abs(Rational(o) - vN).evalf() for o in opts]
    best = min(diffs)
    idx = diffs.index(best)
    return idx + 1


def statement(prm):
    b2, p, q = prm['b2'], prm['p'], prm['q']
    opts = choices(prm)
    opt_labels = ['①', '②', '③', '④', '⑤']
    opts_str = ' '.join(f'{lab} {v}' for lab, v in zip(opt_labels, opts))
    return (
        f'직선 y=({p}/{q})x가 쌍곡선 x^2/k - y^2/{b2} = 1의 한 점근선일 때, '
        f'이 쌍곡선의 주축의 길이는? (단, k는 양수이다.)\n{opts_str}'
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
