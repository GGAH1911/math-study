CANDIDATE = 33  # ★원문제 정답 (절대 변경 금지)

import sympy as sp

# 문제의 수학 구조:
#   lim(p1*a_n + q1*b_n) = k1
#   lim(p2*a_n + q2*b_n) = k2
#   극한이 존재한다고 가정하면 lim a_n = A, lim b_n = B 로 두고
#   p1*A + q1*B = k1
#   p2*A + q2*B = k2
#   를 풀어 lim(r*a_n + s*b_n) = r*A + s*B 를 구한다.
#
# 파라미터화:
#   p1, q1, k1 : 첫 번째 극한 조건의 계수/값
#   p2, q2, k2 : 두 번째 극한 조건의 계수/값
#   r,  s      : 최종적으로 구하는 선형결합의 계수 (원문제는 a_n+b_n 이므로 r=s=1)
PARAMS = dict(p1=1, q1=2, k1=9, p2=2, q2=1, k2=90, r=1, s=1)


def solve(prm):
    A, B = sp.symbols('A B')

    eq1 = sp.Eq(prm['p1'] * A + prm['q1'] * B, prm['k1'])
    eq2 = sp.Eq(prm['p2'] * A + prm['q2'] * B, prm['k2'])

    solution = sp.solve([eq1, eq2], [A, B])
    if not solution or A not in solution or B not in solution:
        # 연립방정식이 유일해를 갖지 않으면 문제로 성립하지 않음
        raise ValueError("연립방정식의 해가 유일하게 존재하지 않습니다.")

    A_val = solution[A]
    B_val = solution[B]

    result = prm['r'] * A_val + prm['s'] * B_val

    if not result.is_number or not result.is_real:
        raise ValueError("답이 실수 값으로 확정되지 않습니다.")

    return int(result)


def statement(prm):
    def term(coef, name):
        if coef == 1:
            return name
        if coef == -1:
            return f"-{name}"
        return f"{coef}{name}"

    def combo(c1, c2):
        t1 = term(c1, "a_{n}")
        t2 = term(c2, "b_{n}")
        sign = "+" if c2 >= 0 else "-"
        t2_abs = term(abs(c2), "b_{n}")
        return f"{t1} {sign} {t2_abs}"

    return (
        "두 수열 \\{a_{n}\\}, \\{b_{n}\\}에 대하여\n"
        f"  \\lim_{{n \\to \\infty}} ({combo(prm['p1'], prm['q1'])}) = {prm['k1']}, "
        f"\\lim_{{n \\to \\infty}} ({combo(prm['p2'], prm['q2'])}) = {prm['k2']}\n"
        f"일 때, \\lim_{{n \\to \\infty}} ({combo(prm['r'], prm['s'])})의 값을 구하시오."
    )


print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
