import sympy as sp
import numpy as np

# f(x)의 정의
x = sp.Symbol('x')
f = sp.exp((x+1)**2/25 - 1)

# 주어진 조건 검증: f(5x-1) = e^(x^2-1)
x_var = sp.Symbol('x')
f_composite = f.subs(x, 5*x_var - 1)
expected = sp.exp(x_var**2 - 1)
composite_simplified = sp.simplify(f_composite - expected)
if composite_simplified == 0:
    print('조건 검증: OK')
else:
    print('조건 검증: FAIL')

# f'(4) 계산
f_prime = sp.diff(f, x)
f_prime_at_4 = f_prime.subs(x, 4)
f_prime_at_4_simplified = sp.simplify(f_prime_at_4)

# 답이 2/5인지 확인
if f_prime_at_4_simplified == sp.Rational(2, 5):
    print('VERIFY_PASS')
else:
    print(f'계산값: {f_prime_at_4_simplified}')
    print('VERIFY_FAIL')