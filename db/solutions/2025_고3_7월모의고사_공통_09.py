import sympy as sp
from sympy import symbols, integrate, diff

a, c, x = symbols('a c x', real=True)

# 이차함수 f(x) = ax^2 + c 정의
f = a*x**2 + c
f_prime = diff(f, x)

# 조건 1 검증: 적분 구간 [-1, 1]에서 f'(x) 적분 = 0
integral_condition = integrate(f_prime, (x, -1, 1))
assert integral_condition == 0, f'Condition failed: {integral_condition}'

# 구하는 값 계산
f_0 = f.subs(x, 0)
f_minus1 = f.subs(x, -1)
term1 = f_0 - f_minus1

integrand = x**2 + 2*x + f_prime
term2 = integrate(integrand, (x, 0, 1))

result = term1 + term2
result_simplified = sp.simplify(result)

if result_simplified == sp.Rational(4, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')