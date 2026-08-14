"""2026 고3 7월 모의고사 공통 1번 — 유리지수 거듭제곱의 곱

원문제: 5^(-1/2) × 25^(3/4) 의 값은?  ① 1 ② √5 ③ 5 ④ 5√5 ⑤ 25

수학 구조: 밑이 같은 두 거듭제곱의 곱.
  a^(e1) × (a^m)^(e2) = a^(e1 + m·e2)
계산한 값을 보기 값들과 대조해 보기 번호를 고른다.
파라미터를 바꾸면 지수 합이 달라져 답(보기 번호)도 달라진다.
"""
from fractions import Fraction
import sympy as sp

CANDIDATE = 3

PARAMS = dict(
    base=5,              # 밑 a
    e1_num=-1,           # 첫째 인수의 지수 분자   → a^(e1_num/e1_den)
    e1_den=2,            # 첫째 인수의 지수 분모
    inner_pow=2,         # 둘째 인수의 밑을 a^inner_pow 로 씀 (25 = 5^2)
    e2_num=3,            # 둘째 인수의 지수 분자   → (a^inner_pow)^(e2_num/e2_den)
    e2_den=4,            # 둘째 인수의 지수 분모
    # 보기 ①~⑤ 의 값을 a^(지수) 형태로 표기한 지수 목록 (1, √5, 5, 5√5, 25)
    choice_exps=[Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2)],
)


def _total_exponent(prm):
    """a^(e1) × (a^m)^(e2) 의 최종 지수 e1 + m·e2 를 유리수로 돌려준다."""
    e1 = sp.Rational(prm['e1_num'], prm['e1_den'])
    e2 = sp.Rational(prm['e2_num'], prm['e2_den'])
    return sp.simplify(e1 + prm['inner_pow'] * e2)


def value(prm):
    """식의 값 (지수법칙으로 정리한 결과)."""
    return sp.simplify(sp.Pow(prm['base'], _total_exponent(prm)))


def solve(prm=None):
    """조건 → 답(보기 번호). 보기 중에 값이 없으면 0."""
    prm = PARAMS if prm is None else prm
    val = value(prm)
    for i, ce in enumerate(prm['choice_exps'], start=1):
        cand = sp.simplify(sp.Pow(prm['base'], sp.Rational(ce.numerator, ce.denominator)))
        if sp.simplify(cand - val) == 0:
            return i
    return 0


def statement(prm=None):
    """새 문제 문장 (보기 포함)."""
    prm = PARAMS if prm is None else prm
    a, m = prm['base'], prm['inner_pow']
    e1 = sp.Rational(prm['e1_num'], prm['e1_den'])
    e2 = sp.Rational(prm['e2_num'], prm['e2_den'])
    def pw(b, e):
        sign = '-' if e < 0 else ''
        e = abs(e)
        exp = f'{sign}\\frac{{{e.p}}}{{{e.q}}}' if e.q != 1 else f'{sign}{e.p}'
        return f'{b}^{{{exp}}}'
    lhs = f'{pw(a, e1)} \\times {pw(a ** m, e2)}'
    marks = '①②③④⑤'
    opts = ' '.join(
        f'{marks[i]} ${sp.latex(sp.simplify(sp.Pow(a, sp.Rational(c.numerator, c.denominator))))}$'
        for i, c in enumerate(prm['choice_exps'])
    )
    return f'${lhs}$ 의 값은? [2점]\n{opts}'


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
