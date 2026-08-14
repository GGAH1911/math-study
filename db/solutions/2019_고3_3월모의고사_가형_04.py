import sympy as sp

# ─────────────────────────────────────────────────────────────
# 문제 구조: f(x) = a*x + sin(b*x) 에 대해
#            lim_{x→c} (f(x)-f(c))/(x-c) = f'(c) = a + b*cos(b*c)
# 원문제는 a=1/2, b=1, c=π 인 특수한 경우 (답: f'(π) = 1/2 + cos π = -1/2)
#
# 파라미터:
#   a : x의 계수 (1차항 기울기)
#   b : sin(bx)의 각주파수 (연쇄법칙 계수)
#   c : 극한을 취하는 점
# 세 값 모두 f'(c)의 값을 바꾸고, 그 결과 5지선다 중 정답 번호(인덱스)도 실제로 바뀐다.
# ─────────────────────────────────────────────────────────────

CANDIDATE = 5  # ★원문제 정답: ⑤

PARAMS = dict(
    a=sp.Rational(1, 2),
    b=1,
    c=sp.pi,
)


def value(prm):
    """f'(c) 를 sympy로 실제 미분·대입해서 구한다 (수학적 답)."""
    a, b, c = prm['a'], prm['b'], prm['c']
    x = sp.Symbol('x')
    f = a * x + sp.sin(b * x)
    fp = sp.diff(f, x)
    return sp.nsimplify(sp.simplify(fp.subs(x, c)))


def choices(prm):
    """정답 value(prm)와, 흔한 계산 실수(1차항 계수/삼각함수항 계수를 잘못
    적용하는 패턴)로 나온 오답들을 함께 생성해 보기 5개를 만든다.
    (k, m) = (a항에 곱하는 정수 계수, cos항에 곱하는 정수 계수).
    (1,1)이 실제 정답 공식 a + b*cos(b*c) 이고 나머지는 대표적 오답 패턴이다."""
    a, b, c = prm['a'], prm['b'], prm['c']
    C = b * sp.cos(b * c)
    pairs = [(-3, 1), (0, 2), (-1, 1), (2, 2), (1, 1)]  # 마지막이 정답 패턴
    raw = [sp.nsimplify(sp.simplify(k * a + m * C)) for k, m in pairs]
    correct = raw[-1]

    # 정답 패턴이 실제 value(prm)과 일치하는지 확인 (값에서 유도했음을 보증)
    if sp.simplify(correct - value(prm)) != 0:
        raise ValueError('정답 패턴이 실제 계산값과 불일치')

    srt = sorted(set(raw))
    if len(srt) != 5:
        raise ValueError('보기 값이 중복되어 5지선다 문제로 성립하지 않습니다')
    return srt, correct


def solve(prm):
    """보기 목록에서 정답이 몇 번째(①~⑤)인지 반환."""
    srt, correct = choices(prm)
    return srt.index(correct) + 1


def statement(prm):
    a, b, c = prm['a'], prm['b'], prm['c']
    x = sp.Symbol('x')
    f = a * x + sp.sin(b * x)
    srt, _correct = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{circled[i]} {sp.latex(v)}' for i, v in enumerate(srt))
    cl = sp.latex(c)
    return (
        f"함수 f(x)={sp.latex(f)}에 대하여 "
        f"\\lim_{{x\\to {cl}}}\\frac{{f(x)-f({cl})}}{{x-{cl}}}의 값은? [3점]\n"
        f"{opts}"
    )


# 원문제 보기와 정확히 일치하는지 고정 (a=1/2, b=1, c=π 일 때)
_default_srt, _ = choices(PARAMS)
assert _default_srt == [sp.Rational(-5, 2), sp.Integer(-2), sp.Rational(-3, 2),
                         sp.Integer(-1), sp.Rational(-1, 2)]

if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
