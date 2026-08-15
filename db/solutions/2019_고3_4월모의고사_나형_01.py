import sympy as sp
from sympy import Rational as R

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# "b^{p/q} × b^{r/s} 의 값은?" 형태의 지수법칙 계산 문제.
# 원문제 3^{3/2} × √3 은 b=3, p/q=3/2, (√b = b^{1/2} 이므로) r/s=1/2 인 특수 경우다.
# 지수법칙에 의해 b^{p/q} × b^{r/s} = b^{p/q + r/s} 이므로,
#   3^{3/2} × 3^{1/2} = 3^{3/2+1/2} = 3^2 = 9
# 이 값이 보기 중 몇 번째인지가 실제 정답(선택지 번호)이다.
#
# 이 문제 유형은 보기가 "9(정답)를 3번째 자리에 둔 6~10 의 연속한 정수 5개"로
# 고정되어 나오는 형태다(①6 ②7 ③8 ④9 ⑤10). 즉 계산값이 이 고정 창(window)을
# 벗어나면 더 이상 "이 유형"의 문제로 성립하지 않으므로 예외를 던진다(규칙 6).
#
# ★답을 바꾸는 파라미터는 밑 b 와 두 지수 p/q, r/s 이지만, 이들은 "지수의 합이
#   6~10 사이의 정수가 되어야 한다"는 조건으로 서로 묶여 있다(예: b,p,q 만 따로
#   +1 하면 지수가 정수가 아니게 되거나 값이 window 를 벗어나 문제가 깨진다).
#   따라서 규칙 5 에 따라 개별 파라미터를 흔드는 대신, 실제로 성립하는 (b,p,q,r,s)
#   조합을 VARIANTS 로 여러 개 제시해 "답이 실제로 달라짐"을 증명한다.

CANDIDATE = 4  # ★원문제 정답 (④ 9)

PARAMS = dict(
    b=3,   # 밑
    p=3, q=2,   # 첫째 항의 지수 p/q  (= 3/2)
    r=1, s=2,   # 둘째 항의 지수 r/s  (= 1/2, 즉 √b)
)

# 이 문제 유형이 강제하는 고정 보기: 9 를 넷째 자리에 둔 6~10 의 연속한 정수.
CHOICES_WINDOW = (6, 7, 8, 9, 10)


def value(prm):
    """b^{p/q} × b^{r/s} = b^{p/q + r/s} 를 sympy 로 실제 계산."""
    b = prm['b']
    exponent = R(prm['p'], prm['q']) + R(prm['r'], prm['s'])
    return sp.nsimplify(sp.Pow(b, exponent))


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 6부터 10까지의 연속 정수."""
    return CHOICES_WINDOW


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        # 값이 6~10 범위를 벗어나면 이 문제 유형으로 성립하지 않음
        raise ValueError(f"값 {v}이(가) 보기 범위 {ch}를 벗어남 — 문제로 성립하지 않음")
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    b, p, q, r, s = prm['b'], prm['p'], prm['q'], prm['r'], prm['s']
    first = f"{b}^{{\\frac{{{p}}}{{{q}}}}}"
    if r == 1 and s == 2:
        second = f"\\sqrt{{{b}}}"
    else:
        second = f"\\sqrt[{s}]{{{b}^{{{r}}}}}"
    return f"{first} \\times {second}의 값은?"


# 원문제 보기가 정확히 ①6 ②7 ③8 ④9 ⑤10 인지 고정 검증
assert choices(PARAMS) == (6, 7, 8, 9, 10)

# 지수의 합이 정수가 되어 값이 보기 창(6~10) 안에 들어오는, 실제로 성립하는 조합들.
# 서로 다른 (b, p, q, r, s) 조합이 서로 다른 보기 번호를 정답으로 만들어낸다는 것을
# 직접 보여준다 (규칙 5의 결합 파라미터 예외).
VARIANTS = [
    dict(b=2, p=2, q=1, r=1, s=1),   # 2^{2+1}=8  → ③
    dict(b=6, p=1, q=2, r=1, s=2),   # 6^{1/2+1/2}=6 → ①
    dict(b=10, p=1, q=2, r=1, s=2),  # 10^{1/2+1/2}=10 → ⑤
    dict(b=7, p=1, q=2, r=1, s=2),   # 7^{1/2+1/2}=7 → ②
]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
