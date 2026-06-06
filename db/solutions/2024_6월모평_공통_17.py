from sympy import *
x = symbols('x')
f = 2*x**4 - x + 3
f_prime = diff(f, x)
# 원래 조건 검증
assert f_prime == 8*x**3 - 1, f'Derivative check failed: {f_prime}'
assert f.subs(x, 0) == 3, f'Initial condition failed: {f.subs(x, 0)}'
# 최종 답 검증
result = f.subs(x, 2)
assert result == 33, f'f(2) = {result}'
print('VERIFY_PASS')