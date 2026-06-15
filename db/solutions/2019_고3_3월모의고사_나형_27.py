"""2019 고3 3월모의고사 나형 27번 — 파라미터 솔버 (수동 작성).
문제: 모든 항 실수인 등비수열 {a_n}, a_2+a_3=1, a_6-a_4=18. 1/a_1 의 값. (답 12)
구조: a_n=a_1 r^{n-1}. a_1 r(1+r)=1, a_1 r^3(r^2-1)=18.
      두 식 나누면 r^2(r-1)=18 → 실근 r=3. a_1·3·4=1 → a_1=1/12 → 1/a_1=12.
재생산: (a_2+a_3, a_6-a_4) 파라미터화.
"""
import sympy as sp


def solve(s_23, d_64):
    a1, r = sp.symbols('a1 r', real=True)
    e1 = sp.Eq(a1 * r + a1 * r ** 2, s_23)        # a_2 + a_3
    e2 = sp.Eq(a1 * r ** 5 - a1 * r ** 3, d_64)    # a_6 - a_4
    for a1v, rv in sp.solve([e1, e2], [a1, r]):
        if rv.is_real and a1v != 0:
            return sp.nsimplify(1 / a1v)


CANDIDATE = 12
assert solve(1, 18) == CANDIDATE, solve(1, 18)
print('VERIFY_PASS')
