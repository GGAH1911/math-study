from sympy import symbols, diff, Rational

# 원문제: f(x) = 10x^2 + 12x 에서 f'(5) 의 값을 구하시오.
# 수학 구조: f(x) = a*x^2 + b*x  (이차항 계수 a, 일차항 계수 b) 이고
#            평가 지점 c 에서의 도함수 값 f'(c) = 2*a*c + b 를 구한다.
# a, b, c 세 파라미터가 모두 답을 바꾼다.
CANDIDATE = 112

PARAMS = dict(a=10, b=12, c=5)


def solve(prm):
    a, b, c = prm['a'], prm['b'], prm['c']
    x = symbols('x')
    f = a * x**2 + b * x
    f_prime = diff(f, x)
    f_prime_at_c = f_prime.subs(x, c)
    return f_prime_at_c


def statement(prm):
    a, b, c = prm['a'], prm['b'], prm['c']

    def term(coef, power):
        if power == 2:
            return f"{coef}x^{{2}}"
        return f"{coef}x"

    return (
        f"함수 f(x)={term(a, 2)}+{term(b, 1)}에 대하여 "
        f"f'({c})의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
