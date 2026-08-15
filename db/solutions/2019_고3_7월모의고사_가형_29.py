import sympy as sp

# [원문제] 반지름 r=1인 원 위의 서로 다른 세 점 A,B,C가
#   x*OA + a*OB + b*OC = 0  (x>0)
# 를 만족할 때 OA·OB 가 최대이면 삼각형 ABC 의 넓이를 S라 하고, M*S 를 구한다.
# (원문제: a=5, b=3, r=1, M=50)
CANDIDATE = 60

# 수학 구조를 드러내는 파라미터
#   a, b : 조건식 x*OA + a*OB + b*OC = 0 의 계수 (a>b>0 이어야 양수 x 실근 존재)
#   r    : 원의 반지름
#   M    : 마지막에 넓이 S 에 곱하는 배수 ("M*S 의 값을 구하시오")
PARAMS = dict(a=5, b=3, r=1, M=50)


def solve(prm):
    a = sp.nsimplify(prm['a'])
    b = sp.nsimplify(prm['b'])
    r = sp.nsimplify(prm['r'])
    M = sp.nsimplify(prm['M'])

    if a <= 0 or b <= 0 or a <= b:
        # x^2 = a^2+b^2+2ab*q (|q|<=1) 이 양수이려면, 그리고 최적점에서
        # x=sqrt(a^2-b^2) 가 실수이려면 a>b>0 이 필요하다.
        raise ValueError('a > b > 0 이어야 조건을 만족하는 양수 x 가 존재한다')

    q = sp.symbols('q', real=True)

    # x*OA + a*OB + b*OC = 0 을 OA, OB, OC 각각과 내적한 세 식을 연립하면
    #   x^2 = a^2 + b^2 + 2ab*q   (q = OB·OC, 단위벡터 기준)
    #   p(q) = OA·OB = -(a + b*q) / x
    # 로 정리된다. p(q) 를 sympy 로 실제로 미분해 임계점을 구한다.
    x_expr = sp.sqrt(a**2 + b**2 + 2 * a * b * q)
    p_expr = -(a + b * q) / x_expr

    crit = sp.solve(sp.Eq(sp.diff(p_expr, q), 0), q)
    crit = [c for c in crit if c.is_real and -1 < c < 1]
    if not crit:
        raise ValueError('OA·OB 를 최대화하는 임계점이 존재하지 않는다')
    q_star = max(crit, key=lambda c: p_expr.subs(q, c))

    x_star = sp.simplify(x_expr.subs(q, q_star))
    p_star = sp.simplify(p_expr.subs(q, q_star))
    s_star = sp.simplify(-(a * q_star + b) / x_star)  # OA·OC (단위벡터 기준)

    # 단위원 위 좌표계: OA=(1,0), OC=(s_star, sqrt(1-s_star^2))
    A = sp.Matrix([1, 0])
    Cy = sp.sqrt(1 - s_star**2)
    if Cy == 0:
        raise ValueError('세 점이 퇴화(일직선)되어 삼각형을 이루지 못한다')
    C = sp.Matrix([s_star, Cy])

    # OB = (p_star, t) 이고 OB·OC = q_star 를 만족하는 t 를 실제로 방정식으로 풀어 구한다.
    t = sp.symbols('t', real=True)
    t_sol = sp.solve(sp.Eq(p_star * s_star + t * Cy, q_star), t)
    if not t_sol:
        raise ValueError('OB 를 결정하는 t 를 구할 수 없다')
    B = sp.Matrix([p_star, t_sol[0]])

    if sp.simplify(B[0]**2 + B[1]**2 - 1) != 0:
        raise ValueError('OB 가 단위벡터 조건을 만족하지 않는다')

    A, B, C = r * A, r * B, r * C
    AB, AC = B - A, C - A
    area = sp.Rational(1, 2) * sp.Abs(AB[0] * AC[1] - AB[1] * AC[0])

    ans = sp.simplify(M * area)
    if not ans.is_number or ans.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError(f'유효한 수치해가 아니다: {ans}')
    return sp.nsimplify(ans)


def statement(prm):
    a, b, r, M = prm['a'], prm['b'], prm['r'], prm['M']
    return (
        f"중심이 O이고 반지름의 길이가 {r}인 원이 있다. 양수 x에 대하여 원 위의 서로 다른 세 점 "
        f"A, B, C가 x·OA + {a}·OB + {b}·OC = 0 을 만족시킨다. OA·OB의 값이 최대일 때, "
        f"삼각형 ABC의 넓이를 S라 하자. {M}S의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
