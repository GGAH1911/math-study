from sympy import symbols, Eq, solve as sp_solve, Rational

CANDIDATE = 3  # ★원문제 정답 - 절대 바꾸지 않음

# 문제의 수학 구조: 등차수열 {a_n}에서 두 항의 번호(n2, n4)와 그 값(val2, val4)이 주어지면
# 공차 d 는 (val4 - val2) / (n4 - n2) 로 정해진다.
# 원문제: a_2 = 3, a_4 = 9 → n2=2, val2=3, n4=4, val4=9
PARAMS = dict(n2=2, val2=3, n4=4, val4=9)


def solve(prm):
    a1, d = symbols('a1 d')
    n2, val2, n4, val4 = prm['n2'], prm['val2'], prm['n4'], prm['val4']
    if n2 == n4:
        raise ValueError('두 항의 번호가 같으면 공차를 결정할 수 없다')
    # 등차수열 일반항: a_n = a1 + (n-1)d
    eq1 = Eq(a1 + (n2 - 1) * d, val2)
    eq2 = Eq(a1 + (n4 - 1) * d, val4)
    sol = sp_solve([eq1, eq2], [a1, d])
    if d not in sol:
        raise ValueError('연립방정식의 해가 존재하지 않는다')
    return sol[d]


def statement(prm):
    return (
        f"등차수열 {{a_n}}에 대하여 a_{prm['n2']} = {prm['val2']}, "
        f"a_{prm['n4']} = {prm['val4']}일 때, 수열 {{a_n}}의 공차는?"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
