import sympy as sp
from sympy import symbols, ln, diff, E

CANDIDATE = 4

# 함수 정의
x = symbols('x', positive=True, real=True)
f = x**3 * ln(x)

# 도함수 구하기
f_prime = diff(f, x)

# x=e에서 도함수 값
f_prime_at_e = f_prime.subs(x, E)

# 최종 값
result = f_prime_at_e / E**2
result_simplified = sp.simplify(result)

# 검증
if result_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')