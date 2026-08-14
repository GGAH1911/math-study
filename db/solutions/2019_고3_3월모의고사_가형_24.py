from sympy import ln, exp, diff, symbols, integrate, Eq, simplify, Rational
from sympy import solve as sp_solve

CANDIDATE = 13  # ★원문제 정답: f(e^3) = 13

# 문제의 수학 구조: f'(x) = k/x, f(1) = c 일 때 f(e^a) 를 구하는 문제.
#   f(x) = k*ln(x) + C 이고 f(1)=c 로 C=c 가 정해지므로 f(e^a) = k*a + c.
# 원문제는 k=1, c=10, a=3 인 경우 (답 13).
PARAMS = dict(
    k=1,       # f'(x) = k/x 의 계수
    c=10,      # 초기조건 f(1) = c
    a=3,       # 구하려는 값 f(e^a)
)


def solve(prm):
    k = prm['k']
    c = prm['c']
    a = prm['a']

    x = symbols('x', positive=True, real=True)
    C = symbols('C', real=True)

    # f'(x) = k/x 를 부정적분하여 f(x) 를 구함
    f_prime = k / x
    f = integrate(f_prime, x) + C  # f(x) = k*ln(x) + C

    # 도함수 조건 검증: d/dx f = f'(x)
    if simplify(diff(f, x) - f_prime) != 0:
        raise ValueError('도함수 조건을 만족하지 않습니다.')

    # 초기조건 f(1) = c 로 C 결정
    eq = Eq(f.subs(x, 1), c)
    sols = sp_solve(eq, C)
    if not sols:
        raise ValueError('초기조건을 만족하는 C가 존재하지 않습니다.')
    C_val = sols[0]
    f_solved = f.subs(C, C_val)

    # f(e^a) 계산
    result = simplify(f_solved.subs(x, exp(a)))
    if not result.is_number:
        raise ValueError('결과가 수치로 확정되지 않았습니다.')

    result = simplify(result)
    if result == int(result):
        return int(result)
    return result


def statement(prm):
    k = prm['k']
    c = prm['c']
    a = prm['a']
    return (
        f"함수 f(x)의 도함수가 f'(x) = \\frac{{{k}}}{{x}} 이고 f(1)={c} 일 때, "
        f"f(e^{a})의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
