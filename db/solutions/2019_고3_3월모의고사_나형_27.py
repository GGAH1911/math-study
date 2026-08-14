"""2019 고3 3월모의고사 나형 27번 — 파라미터화 솔버.

문제 구조:
  모든 항이 실수인 등비수열 {a_n} (첫째항 a1, 공비 r)에서
    a_3 + a_2 = s   ...(첫 조건 값)
    a_6 - a_4 = d   ...(둘째 조건 값)
  일 때 1/a_1 의 값을 구하시오.

  a_2 + a_3 = a1*r*(1+r) = s
  a_6 - a_4 = a1*r^3*(r^2-1) = d

두 식을 나누면 r^2*(r-1) = d/s 인 삼차방정식이 되고, 실근 r 에 대응하는
a1 이 유일하게(0이 아니게) 정해질 때만 문제가 성립한다.

파라미터로 뽑은 수학 구조: s(=a_2+a_3), d(=a_6-a_4). 이 둘은 방정식의
우변 상수이며, 값을 바꾸면 삼차방정식의 근(공비 r)과 첫째항 a1이 통째로
바뀌어 1/a_1 값이 달라진다 (예: (s,d)=(1,18)→12, (1,4)→6, (1,48)→20).
"""
import sympy as sp


def solve(prm):
    s, d = prm['s'], prm['d']
    a1, r = sp.symbols('a1 r', real=True)
    e1 = sp.Eq(a1 * r + a1 * r ** 2, sp.Rational(s))        # a_2 + a_3 = s
    e2 = sp.Eq(a1 * r ** 5 - a1 * r ** 3, sp.Rational(d))    # a_6 - a_4 = d

    sols = sp.solve([e1, e2], [a1, r])
    valid = []
    for a1v, rv in sols:
        if rv.is_real and rv != 0 and a1v != 0:
            valid.append(a1v)

    if len(valid) != 1:
        # 실수 등비수열 조건을 만족하는 (a1, r) 이 없거나 유일하지 않으면
        # 이 파라미터 조합은 원문제와 같은 형태의 문제로 성립하지 않는다.
        raise ValueError(
            f"파라미터 조합(s={s}, d={d})에서 실수 등비수열 해가 유일하지 않습니다: {valid}"
        )

    return sp.nsimplify(1 / valid[0])


def statement(prm):
    s, d = prm['s'], prm['d']
    return (
        "모든 항이 실수인 등비수열 {a_n}에 대하여\n"
        f"  a_3 + a_2 = {s},  a_6 - a_4 = {d}\n"
        "일 때, 1/a_1 의 값을 구하시오."
    )


PARAMS = dict(s=1, d=18)   # 원문제: a_3+a_2=1, a_6-a_4=18

CANDIDATE = 12

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
