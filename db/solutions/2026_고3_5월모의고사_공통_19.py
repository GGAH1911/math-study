import sympy as sp

CANDIDATE = 10

# 문제: x^3 - sq_coeff*a*x^2 + const_coeff*a^2 = 0 의 서로 다른 양의 실근의
# 개수가 1일 때, 양수 a 의 값을 구하시오.
#   sq_coeff    : x^2 항 계수(a 에 곱해지는 계수) — 원문제 "3a"
#   const_coeff : 상수항 계수(a^2 에 곱해지는 계수) — 원문제 "40a^2"
PARAMS = dict(
    sq_coeff=3,
    const_coeff=40,
)


def solve(prm):
    x = sp.Symbol('x')
    a = sp.Symbol('a')
    sq_coeff = sp.nsimplify(prm['sq_coeff'])
    const_coeff = sp.nsimplify(prm['const_coeff'])

    f = x**3 - sq_coeff * a * x**2 + const_coeff * a**2
    fp = sp.diff(f, x)

    # 극점: x=0 과 나머지 하나(둘 다 a 에 대한 식)
    crit = sp.solve(sp.Eq(fp, 0), x)
    nonzero_crit = [c for c in crit if c != 0][0]

    # f(0) = const_coeff*a^2 > 0 (a>0, const_coeff>0 이면 극대, 항상 양수)
    # 이므로 양의 실근이 "정확히 1개"가 되려면 나머지 극점(극소)의 함숫값이
    # 0이어서 그 지점이 중근(=유일한 양의 실근)이 되어야 한다.
    f_at_nonzero = sp.expand(f.subs(x, nonzero_crit))
    candidates = sp.solve(sp.Eq(f_at_nonzero, 0), a)
    positive_candidates = [c for c in candidates if c.is_real and c > 0]

    # 후보 a 값마다 실제로 서로 다른 양의 실근이 1개인지 직접 검증
    verified = []
    for a_val in positive_candidates:
        f_num = f.subs(a, a_val)
        roots = sp.solve(sp.Eq(f_num, 0), x)
        pos_roots = set(r for r in roots if r.is_real and r > 0)
        if len(pos_roots) == 1:
            verified.append(a_val)

    assert len(verified) == 1, f"조건을 만족하는 양수 a가 유일하지 않음: {verified}"
    return verified[0]


def statement(prm):
    return (
        f"x에 대한 방정식 x^3 - {prm['sq_coeff']}ax^2 + {prm['const_coeff']}a^2 = 0의 "
        "서로 다른 양의 실근의 개수가 1일 때, 양수 a의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
