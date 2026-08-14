"""2026 고3 7월 공통 7번 — 정적분 관계식으로 미정계수 구하기 (파라미터 솔버).

원문제: f(x) = x^3 + x^2 + a 에 대하여
        ∫_0^2 f(x)dx = 40/3 + ∫_0^(-2) f(x)dx  일 때 상수 a 의 값은?

구조: f(x) = c3·x^3 + c2·x^2 + a (a 는 미지의 상수)
      ∫_0^U f dx = K + ∫_0^L f dx  를 a 에 대해 푼다.
      객관식이므로 구한 a 를 보기 목록과 대조해 보기 번호를 답으로 낸다.
"""
from sympy import symbols, integrate, Rational, Eq, solve as sym_solve, nsimplify, latex

CANDIDATE = 2

PARAMS = dict(
    c3=1,                 # x^3 의 계수
    c2=1,                 # x^2 의 계수
    upper=2,              # 좌변 정적분의 위끝 (아래끝은 0)
    lower=-2,             # 우변 정적분의 위끝 (아래끝은 0)
    const=Rational(40, 3),  # 우변에 더해진 상수 K
    choices=[Rational(11, 6), Rational(2), Rational(13, 6), Rational(7, 3), Rational(5, 2)],
)


def solve_value(prm):
    """조건식을 만족하는 상수 a 의 값(수학적 답)."""
    x, a = symbols('x a')
    f = prm['c3'] * x**3 + prm['c2'] * x**2 + a
    lhs = integrate(f, (x, 0, prm['upper']))
    rhs = prm['const'] + integrate(f, (x, 0, prm['lower']))
    sols = sym_solve(Eq(lhs, rhs), a)
    if not sols:
        raise ValueError('a 에 대해 풀리지 않는 조건식')
    return nsimplify(sols[0])


def solve(prm):
    """객관식 답 — 구한 a 가 보기에 있으면 그 보기 번호를, 없으면 a 값 자체를 돌려준다."""
    val = solve_value(prm)
    for i, c in enumerate(prm.get('choices') or [], start=1):
        if nsimplify(c) == val:
            return i
    return val


def statement(prm):
    """새 문제 문장(보기 포함)."""
    x = symbols('x')
    f = prm['c3'] * x**3 + prm['c2'] * x**2
    body = (f'함수 f(x)={latex(f)}+a 에 대하여 '
            f"\\int_{{0}}^{{{prm['upper']}}}f(x)dx={latex(prm['const'])}"
            f"+\\int_{{0}}^{{{prm['lower']}}}f(x)dx 일 때, 상수 a 의 값은?")
    marks = '①②③④⑤'
    opts = ''.join(f'{marks[i]}{latex(c)}' for i, c in enumerate(prm.get('choices') or []))
    return body + '\n' + opts


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
