import sympy as sp
from sympy import exp, ln, diff, solve

# 함수 f(x) 정의
x = sp.Symbol('x')
f = 1 / (exp(x) + 2)

# f'(x) 계산
f_prime = diff(f, x)

# g(1/4)를 구하기: f(a) = 1/4인 a를 찾기
eq = f - sp.Rational(1, 4)
a_val = solve(eq, x)[0]  # ln(2)

# f'(ln(2)) 계산
f_prime_at_ln2 = f_prime.subs(x, a_val)

# g'(1/4) = 1/f'(g(1/4)) = 1/f'(ln(2))
g_prime_at_quarter = 1 / f_prime_at_ln2

# 최종 답
result = float(g_prime_at_quarter)

if result == -8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')