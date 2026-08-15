"""2019 고3 4월모의고사 나형 22번 — 파라미터화 솔버.

문제: 공비가 r인 등비수열 {a_n}에 대하여 a_i/a_j의 값을 구하시오. (단, a_j ≠ 0)
수학 구조: a_n = a_1 * r^(n-1) 이므로
    a_i / a_j = r^(n-1) 아래 첨자 곱 관계 → a_1*r^(i-1) / (a_1*r^(j-1)) = r^(i-j)
즉 답은 "공비 r" 과 "두 항의 인덱스 차 (i-j)" 로만 결정된다.
파라미터:
  r : 등비수열의 공비  (원문제 5)
  i : 분자 항의 첨자   (원문제 5)
  j : 분모 항의 첨자   (원문제 3)
r, i, j 모두 답 r^(i-j) 을 실제로 바꾼다(각각 독립적으로 지수/밑을 바꾸므로).
"""
import sympy as sp


def solve(prm):
    r, i, j = prm['r'], prm['i'], prm['j']
    a1 = sp.symbols('a1', nonzero=True)
    n = sp.symbols('n')
    a = lambda k: a1 * r ** (k - 1)          # 등비수열 일반항 a_n = a_1 * r^(n-1)
    return sp.simplify(a(i) / a(j))          # a_i/a_j = r^(i-j)


def statement(prm):
    r, i, j = prm['r'], prm['i'], prm['j']
    return (f"공비가 {r}인 등비수열 {{a_n}}에 대하여 "
            f"a_{{{i}}}/a_{{{j}}}의 값을 구하시오. (단, a_{{{j}}} ≠ 0)")


CANDIDATE = 25
PARAMS = dict(r=5, i=5, j=3)

assert solve(PARAMS) == CANDIDATE, solve(PARAMS)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
