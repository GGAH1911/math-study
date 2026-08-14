import sympy as sp

x = sp.Symbol('x')

# ---------------------------------------------------------------------------
# 문제 구조
#   lim_{x->0} (e^{a x} - 1) / (b x) = a / b   (로피탈 정리)
#
# 보기는 "분모 b는 고정한 채, 분자를 연속한 정수 g, g+1, ..., g+4 로 두고
#          b로 나눈 다섯 개의 값"으로 구성된다.
#   원문제: b=3, g=3  ->  {3,4,5,6,7}/3 = {1, 4/3, 5/3, 2, 7/3}
#   정답 a=4 는 이 정수 구간 [g, g+4] 안에서 g로부터 (a-g) 만큼 떨어진 위치,
#   즉 보기 번호 = a - g + 1 번째.
#
# 답을 실제로 바꾸는 파라미터:
#   - a (지수 계수, 분자) : 정수 구간 내에서 a의 위치가 달라지면 보기 번호가 바뀐다.
#   - g (보기 구간의 시작 정수) : 구간이 옮겨지면 같은 a라도 보기 번호가 바뀐다.
#   - b (분모 계수) : 극한값 자체(value)와 보기의 실제 수치를 바꾼다.
# ---------------------------------------------------------------------------

CANDIDATE = 2  # ★원문제 정답: ② (절대 바꾸지 않음)

PARAMS = dict(
    a=4,   # e^{a x} 의 지수 계수
    b=3,   # 분모 b x 의 계수
    g=3,   # 보기 구간 [g, g+4] (정수 5개, b로 나눈 값이 보기)
)


def value(prm):
    """sympy로 실제 극한을 계산해 수학적 답(a/b)을 구한다."""
    a, b = prm['a'], prm['b']
    if b == 0:
        raise ValueError("분모 계수 b는 0이 될 수 없습니다.")
    f = (sp.exp(a * x) - 1) / (b * x)
    v = sp.limit(f, x, 0)
    if not v.is_rational:
        raise ValueError("극한값이 유리수가 아닙니다: 문제 조건 위반")
    return sp.nsimplify(v)


def choices(prm):
    """정답을 유도한 값에서 보기 목록을 만든다: 연속 정수 g..g+4 를 b로 나눈 값들."""
    b, g = prm['b'], prm['g']
    if b == 0:
        raise ValueError("분모 계수 b는 0이 될 수 없습니다.")
    numerators = [g + i for i in range(5)]
    ch = [sp.Rational(n, b) for n in numerators]
    if len(set(ch)) != 5:
        raise ValueError("보기 다섯 개가 서로 겹칩니다: 문제 조건 위반")
    return ch


def solve(prm):
    """보기 목록에서 정답 값이 위치한 번호(1~5)를 찾는다."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        # a가 [g, g+4] 정수 구간 밖에 있어 어느 보기와도 정확히 일치하지 않음
        raise ValueError(f"값 {v} 이(가) 보기 {ch} 안에 없습니다: 성립하지 않는 조합입니다.")
    return ch.index(v) + 1


def statement(prm):
    a, b, g = prm['a'], prm['b'], prm['g']
    ch = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    ch_str = "  ".join(f"{lab} {sp.latex(c)}" for lab, c in zip(labels, ch))
    return (
        f"lim_{{x \\to 0}} \\frac{{e^{{{a}x}}-1}}{{{b}x}} 의 값은?\n"
        f"  {ch_str}"
    )


# 원문제 보기가 정확히 재현되는지 고정
assert choices(dict(a=4, b=3, g=3)) == [
    sp.Rational(1, 1), sp.Rational(4, 3), sp.Rational(5, 3),
    sp.Rational(2, 1), sp.Rational(7, 3),
]

print(statement(PARAMS))
print('answer index =', solve(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
