import sympy as sp

# 원문제: f(x) = x^3 + 4*sqrt(x) 에서 f'(4) 의 값을 구하시오.
#
# 수학 구조: f(x) = a*x^n + b*sqrt(x) 형태의 함수를 점 c 에서 미분한 값을 구하는 문제.
#   - a, n : x^n 항의 계수·차수
#   - b    : sqrt(x) 항의 계수
#   - c    : 도함수를 평가하는 점 (양수)
# f'(x) = a*n*x^(n-1) + (b/2)*x^(-1/2) 이고, 이 식에 x=c 를 대입해 답을 얻는다.

CANDIDATE = 49

PARAMS = dict(a=1, n=3, b=4, c=4)


def solve(prm):
    a, n, b, c = prm['a'], prm['n'], prm['b'], prm['c']
    if c <= 0:
        raise ValueError('sqrt(x) 항이 정의되려면 평가점 c 는 양수여야 합니다.')
    x = sp.Symbol('x', positive=True)
    f = a * x**n + b * sp.sqrt(x)
    f_prime = sp.diff(f, x)
    val = f_prime.subs(x, c)
    val = sp.nsimplify(val)
    if not val.is_number or val.has(sp.zoo, sp.nan, sp.oo, sp.I):
        raise ValueError(f'유효한 값이 아닙니다: {val}')
    return val


def statement(prm):
    a, n, b, c = prm['a'], prm['n'], prm['b'], prm['c']
    a_str = '' if a == 1 else str(a)
    return (
        f"함수 f(x)={a_str}x^{n}+{b}\\sqrt{{x}} 에 대하여 f'({c}) 의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
