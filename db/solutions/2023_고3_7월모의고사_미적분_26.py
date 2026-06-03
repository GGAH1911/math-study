import sympy as sp
from sympy import symbols, integrate, diff, Rational

x = symbols('x')

# 조건을 만족하는 함수: f(x) = 4x
f = 4*x
f_prime = diff(f, x)

# 조건 1: f(1) = 4 확인
condition1 = f.subs(x, 1)
assert condition1 == 4, f'f(1) = {condition1}, expected 4'

# 조건 2: 적분 조건 확인
integral_check = integrate((x - 1) * f_prime.subs(x, x/2), (x, 1, 2))
assert integral_check == 2, f'integral = {integral_check}, expected 2'

# 답 계산
answer = integrate(f, (x, Rational(1,2), 1))
assert answer == Rational(3, 2), f'answer = {answer}, expected 3/2'

print('VERIFY_PASS')