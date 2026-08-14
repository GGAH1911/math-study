"""2019 고3 3월모의고사 나형 26번 — 파라미터화 솔버.

원문제: log_x(-x^2+4x+5) 가 정의되기 위한 모든 정수 x 의 값의 합. (답 9)

수학 구조
---------
로그 log_x(진수) 가 정의되려면
  (1) 밑 조건: x > 0, x ≠ 1               (문제 유형 자체가 고정하는 조건, 파라미터 아님)
  (2) 진수 조건: a·x^2 + b·x + c > 0       (a,b,c 가 문제를 결정하는 진짜 파라미터)

a<0 인 하향 포물선이어야 진수 조건이 유계구간이 되어 "정수의 합"이 유한하게 정의된다.
a,b,c 로부터 sympy 로 부등식을 직접 풀어 유계구간을 얻고, 그 구간과 밑 조건의 교집합에
속하는 정수를 모두 더한다. b, c 를 바꾸면 구간(근의 위치)이 바뀌어 답도 실제로 바뀐다.
"""

import sympy as sp

X = sp.symbols('x', real=True)


def _domain(prm):
    """진수 조건 a x^2+b x+c > 0 의 해집합을 sympy 로 직접 계산."""
    a, b, c = prm['a'], prm['b'], prm['c']
    if a >= 0:
        # a>=0 이면 진수 조건의 해가 무계(반직선/전체)가 되어
        # "정수의 합"이 유한하게 정의되지 않는다 → 문제가 성립하지 않음.
        raise ValueError("a < 0 이어야 진수 조건이 유계구간이 되어 문제가 성립합니다.")
    expr = a * X ** 2 + b * X + c
    dom = sp.solve_univariate_inequality(expr > 0, X, relational=False)
    if not isinstance(dom, sp.Interval):
        raise ValueError("이 파라미터 조합에서는 진수 조건이 단일 유계구간이 아닙니다.")
    if dom.inf in (sp.S.NegativeInfinity, sp.S.Infinity) or dom.sup in (sp.S.NegativeInfinity, sp.S.Infinity):
        raise ValueError("진수 조건의 구간이 무계입니다.")
    return dom


def solve(prm):
    """밑 조건(x>0, x≠1)과 진수 조건 구간의 교집합에 속하는 정수의 합."""
    dom = _domain(prm)
    lo = int(sp.floor(dom.inf)) - 1
    hi = int(sp.ceiling(dom.sup)) + 1
    total = 0
    for xv in range(lo, hi + 1):
        if xv > 0 and xv != 1 and dom.contains(sp.Integer(xv)):
            total += xv
    return total


def statement(prm):
    a, b, c = prm['a'], prm['b'], prm['c']
    expr = sp.expand(a * X ** 2 + b * X + c)
    expr_str = sp.sstr(expr).replace('**', '^').replace('*', '')
    return f"log_x({expr_str})가 정의되기 위한 모든 정수 x의 값의 합을 구하시오."


CANDIDATE = 9
PARAMS = dict(a=-1, b=4, c=5)

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
