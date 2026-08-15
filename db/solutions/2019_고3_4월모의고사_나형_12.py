import sympy as sp
from sympy import symbols, Rational, oo

n = symbols('n', integer=True, positive=True)

# ── 문제의 수학 구조 ────────────────────────────────────────────────
# 원문제: sum_{n=1}^inf (7 - a_n/2^n) = 19 일 때 lim a_n/2^{n+1} 을 구하라.
#
# 핵심 트릭: a_n = C*base^n - b_n 으로 두면 조건식은 sum b_n/base^n = S 가 되고,
# 이 급수가 수렴하려면(필요조건) b_n/base^n -> 0 이어야 한다. 그러면
#   a_n / base^{n+shift} = (C*base^n - b_n) / base^{n+shift} = C/base^shift - (b_n/base^n)/base^shift
#   -> C/base^shift   (n -> ∞)
# 즉 답은 오직 C(첫 괄호 안의 상수), base(거듭제곱의 밑), shift(분모 지수의 오프셋)
# 세 가지에만 의존하고, 급수의 합 S 자체는 답에 전혀 영향을 주지 않는다(문제의 "함정").
#
# 객관식 보기는 등차수열 형태(start, start+step, ..., start+4*step)로 배치되어 있고,
# 그 안에서 실제 값이 몇 번째 자리에 오는지가 정답 번호다.

CANDIDATE = 4  # ★원문제 정답(보기 번호) — 절대 바꾸지 않음

PARAMS = dict(
    C=7,                      # 괄호 안 상수 (7 - a_n/2^n 의 7)
    base=2,                   # 거듭제곱의 밑 (2^n 의 2)
    shift=1,                  # 극한식 분모의 지수 오프셋 (a_n/2^{n+1} 의 +1)
    S=19,                     # 급수의 합(문제 문장용 — 실제 답에는 영향 없음, 함정 장치)
    start=2,                  # 보기(등차수열)의 첫 값
    step=Rational(1, 2),      # 보기(등차수열)의 공차
)


def value(prm):
    """실제로 sympy summation/limit 을 써서 lim a_n/base^{n+shift} 값을 구한다."""
    C, base, shift, S = prm['C'], prm['base'], prm['shift'], prm['S']
    base = sp.nsimplify(base)

    # b_n/base^n 이 0으로 수렴하면서 sum_{n=1}^inf b_n/base^n = S 를 만족하는
    # 구체적인 등비꼴 예시를 하나 구성한다 (문제 조건을 만족하는 a_n 이 존재함을 보임).
    q = Rational(1, 3)  # 0<q<1 인 임의의 공비 — 어떤 값을 잡아도 아래 극한값은 동일해야 함
    term = S * (1 - q) * q ** (n - 1)         # b_n / base^n
    total = sp.summation(term, (n, 1, oo))
    if sp.simplify(total - S) != 0:
        raise ValueError('급수 합 조건을 만족하는 예시 구성 실패')

    b_n = term * base ** n
    a_n = C * base ** n - b_n
    L = sp.limit(a_n / base ** (n + shift), n, oo)
    return sp.nsimplify(L)


def choices(prm):
    """보기 목록 — 값에서(등차수열 규칙으로) 유도."""
    start, step = prm['start'], prm['step']
    return [start + i * step for i in range(5)]


# 원문제 보기(①2 ②5/2 ③3 ④7/2 ⑤4)와 일치하는지 고정
assert choices(PARAMS) == [2, Rational(5, 2), 3, Rational(7, 2), 4]


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if sp.simplify(c - v) == 0:
            return i
    raise ValueError(f'값 {v} 이 보기 {ch} 안에 없음 — 성립하지 않는 파라미터 조합')


def statement(prm):
    C, base, shift, S = prm['C'], prm['base'], prm['shift'], prm['S']
    ch = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opts = '  '.join(f'{lab} {sp.nsimplify(v)}' for lab, v in zip(labels, ch))
    exp_shift = f'n+{shift}' if shift != 1 else 'n+1'
    return (
        f'수열 \\{{a_n\\}}에 대하여 '
        f'\\sum_{{n=1}}^{{\\infty}} \\left( {C} - \\frac{{a_n}}{{{base}^n}} \\right) = {S}일 때, '
        f'\\lim_{{n\\to\\infty}} \\frac{{a_n}}{{{base}^{{{exp_shift}}}}}의 값은?\n'
        f'{opts}'
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
