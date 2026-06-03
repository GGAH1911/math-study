import sympy as sp
from sympy import symbols, ln, limit, diff, simplify

x = symbols('x')
f_prime_0 = 6

# f(x) = f(0) + f'(0)*x + higher order terms
# 검증: f(x) - f(0) = f'(0)*x + o(x)를 극한식에 대입
# lim (f'(0)*x) / ln(1+3x) as x->0

numerator = f_prime_0 * x
denominator = ln(1 + 3*x)

result = limit(numerator / denominator, x, 0)
print(f'limit result: {result}')
if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')