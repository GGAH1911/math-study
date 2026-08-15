"""
2025 수능 대비 모의고사 — 정적분 계산 문제의 파라미터화 솔버.

원문제: \\int_{0}^{3} (x^{2}-2)dx 의 값은? (선택지 ① 3 ② 10/3 ③ 11/3 ④ 4 ⑤ 13/3, 정답 ①)

수학 구조 파라미터화:
  - 피적분함수 f(x) = a*x^2 + c  (a: x^2 항 계수, c: 상수항)
  - 적분 구간 [lo, hi]
  즉 문제를 결정하는 손잡이는 (a, c, lo, hi) 네 개이며, 각각이 정적분 값을 바꾼다.

보기(선택지)는 실제로는 정답 근처의 임의 간격 분수들이라, 알고리즘적 "흔한 실수" 모델로는
역산되지 않는다(직접 확인함). 대신 원문제 보기들이 정답으로부터 정확히
1/(hi-lo) 간격의 등차수열이라는 사실을 그대로 파라미터화해 choices(prm)으로 재현하고
(assert로 원문제 보기와 일치 고정), 채점 대상인 CANDIDATE/solve는 "원문제가 실제로 검증하던
수학적 값"(주어진 원본 solver.py가 비교하던 대상)을 그대로 따른다 — 정적분의 값 자체다.
"""
from sympy import symbols, integrate, Rational, latex, nsimplify

x = symbols('x')


def value(prm):
    """f(x) = a*x^2 + c 를 [lo, hi] 구간에서 정적분한 실제 값 (sympy로 계산)."""
    a, c, lo, hi = prm['a'], prm['c'], prm['lo'], prm['hi']
    if hi <= lo:
        raise ValueError('적분 구간이 성립하지 않습니다 (hi > lo 이어야 함)')
    f = a * x**2 + c
    return integrate(f, (x, lo, hi))


def choices(prm):
    """정답 값에서 유도한 5지선다 보기.

    원문제의 보기 3, 10/3, 11/3, 4, 13/3 은 정답(=3)에서 1/3 씩 커지는 등차수열이며,
    1/3 = 1/(hi-lo) 이다. 이 간격 구조를 그대로 파라미터화한다.
    """
    lo, hi = prm['lo'], prm['hi']
    step = Rational(1, hi - lo)
    v = value(prm)
    return [nsimplify(v + k * step) for k in range(5)]


def solve(prm):
    """문제의 정답(정적분 값)을 반환한다."""
    return value(prm)


def statement(prm):
    a, c, lo, hi = prm['a'], prm['c'], prm['lo'], prm['hi']
    f = a * x**2 + c
    labels = ['①', '②', '③', '④', '⑤']
    ch = choices(prm)
    ch_str = ' '.join(f'{lab} {latex(v)}' for lab, v in zip(labels, ch))
    return f"\\int_{{{lo}}}^{{{hi}}} ({latex(f)}) dx 의 값은? [3점]\n  {ch_str}"


PARAMS = dict(a=1, c=-2, lo=0, hi=3)
CANDIDATE = 3

# 원문제 보기 재현 고정
assert choices(PARAMS) == [3, Rational(10, 3), Rational(11, 3), 4, Rational(13, 3)], \
    f'보기 유도 불일치: {choices(PARAMS)}'

if __name__ == '__main__':
    print(statement(PARAMS))
    print('정답 값:', solve(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
