from sympy import symbols, solve, integrate, sqrt, simplify
import sympy as sp

x = symbols('x')
f = x**3 - 7*x + 6
f_prime = 3*x**2 - 7

# 검증: 함수 조건
assert f.subs(x, 1) == 0, 'f(1) should be 0'
assert f.subs(x, 2) == 0, 'f(2) should be 0'
assert f_prime.subs(x, 0) == -7, "f'(0) should be -7"

# P와 Q 찾기
line_eq = f - 4*x  # x^3 - 11x + 6
roots = solve(line_eq, x)
x_3 = 3  # P의 x좌표
x_Q = (-3 + sqrt(17)) / 2  # Q의 x좌표

# 넓이 계산
integrand_A = x**3 - 11*x + 6
A = integrate(integrand_A, (x, 0, x_Q))

integrand_B = -x**3 + 11*x - 6
B = integrate(integrand_B, (x, x_Q, 3))

result = B - A
result_simplified = simplify(result)

if simplify(result_simplified - sp.Rational(45, 4)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Result: {result_simplified}')