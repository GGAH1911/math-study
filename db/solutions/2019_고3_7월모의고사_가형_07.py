from sympy import symbols, Eq, sqrt, Rational
from sympy import solve as sp_solve

# [수학 구조]
# 두 초점 F(c,0), F'(-c,0)을 갖는 타원 위의 두 점 A,B를 F'을 지나는 직선이 지난다.
# 타원의 정의(|PF|+|PF'|=2a)를 A,B 각각에 적용하면
#   삼각형 ABF의 둘레 = |AF|+|BF|+|AB| = |AF|+|BF|+|AF'|+|BF'| = 4a
# 즉 둘레(perimeter) = 4a  ->  a = perimeter/4
# 그리고 b^2 = a^2 - c^2 (타원의 초점 관계식), 단축의 길이 = 2b
#
# 파라미터로 뽑은 것: c(초점의 x좌표, 반초점거리), perimeter(삼각형 ABF의 둘레)
# 이 둘을 바꾸면 a, b, 단축의 길이가 실제로 달라진다.

CANDIDATE = 24  # 원문제 정답: 단축의 길이 = 24

PARAMS = dict(
    c_val=5,          # 초점 F(c,0), F'(-c,0)의 c
    perimeter=52,      # 삼각형 ABF의 둘레
)


def solve(prm):
    c_val = prm['c_val']
    perimeter = prm['perimeter']

    a, c, b = symbols('a c b', positive=True)

    # 1) 타원의 정의로부터 둘레 = 4a
    a_sol = sp_solve(Eq(4 * a, perimeter), a)
    if not a_sol:
        raise ValueError('둘레 조건으로부터 a를 구할 수 없습니다.')
    a_val = a_sol[0]

    # 2) 초점 관계식 b^2 = a^2 - c^2
    if a_val**2 - c_val**2 <= 0:
        raise ValueError('a^2 <= c^2 이면 타원이 성립하지 않습니다 (b가 실수가 아님).')

    b_sol = sp_solve(Eq(b**2, a_val**2 - c_val**2), b)
    if not b_sol:
        raise ValueError('b를 구할 수 없습니다.')
    b_val = [s for s in b_sol if s > 0][0]

    # 3) 단축의 길이 = 2b
    return 2 * b_val


def statement(prm):
    c_val = prm['c_val']
    perimeter = prm['perimeter']
    return (
        f"두 점 F({c_val}, 0), F'(-{c_val}, 0)을 초점으로 하는 타원이 있다. "
        f"점 F'을 지나고 기울기가 양수인 직선과 타원의 교점을 각각 A, B라 하자. "
        f"삼각형 ABF의 둘레의 길이가 {perimeter}일 때, 타원의 단축의 길이는?"
    )


# 서로 다른 (c_val, perimeter) 조합이 서로 다른 답을 내는지 직접 확인:
# c=5, perimeter=52 -> a=13, b=12, 단축=24 (원문제)
# c=3, perimeter=52 -> a=13, b^2=169-9=160, 단축=2*sqrt(160)
# c=5, perimeter=44 -> a=11, b^2=121-25=96, 단축=2*sqrt(96)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
