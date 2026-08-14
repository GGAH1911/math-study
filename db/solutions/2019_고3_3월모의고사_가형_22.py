"""2019 고3 3월모의고사 가형 22번 — 파라미터화 솔버.

원문제: 함수 f(x)=e^{3x-3}+1 에 대하여 f'(1)의 값을 구하시오. (답 3)

수학 구조:
    f(x) = e^{a*x+b} + c   (지수함수 + 상수, c는 미분하면 사라지는 순수 장식항)
    f'(x) = a * e^{a*x+b}
    f'(x1) = a * e^{a*x1+b}
원문제는 a=3, b=-3, x1=1 로 지수 a*x1+b = 3*1-3 = 0 이 되어
f'(1)=3*e^0=3 이라는 깔끔한 값이 나오도록 설계되어 있다.
a, b, x1 을 각각 움직이면 지수부 a*x1+b 값이 달라지면서 답도 실제로 달라진다
(세 파라미터 모두 답에 영향을 주는 진짜 자유도이다). c는 상수항이라 미분에 영향이
없으므로 문제 겉모습만 바꾸는 장식 파라미터로 남겨둔다.
"""
import sympy as sp

PARAMS = dict(a=3, b=-3, c=1, x1=1)


def solve(prm):
    x = sp.symbols('x')
    f = sp.exp(prm['a'] * x + prm['b']) + prm['c']
    fprime = sp.diff(f, x)
    return sp.simplify(fprime.subs(x, prm['x1']))


def _format_linear(a, b, var='x'):
    """a*x+b 꼴을 'ax + b' 형태의 한국어 수식 문자열로 변환."""
    if a == 1:
        term = f"{var}"
    elif a == -1:
        term = f"-{var}"
    else:
        term = f"{a}{var}"
    if b > 0:
        return f"{term} + {b}"
    elif b < 0:
        return f"{term} - {-b}"
    return term


def statement(prm):
    a, b, c, x1 = prm['a'], prm['b'], prm['c'], prm['x1']
    exponent = _format_linear(a, b)
    c_str = f" + {c}" if c >= 0 else f" - {-c}"
    return (
        f"함수 f(x)=e^{{{exponent}}}{c_str}에 대하여 "
        f"f'({x1})의 값을 구하시오. [3점]"
    )


CANDIDATE = 3

if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
