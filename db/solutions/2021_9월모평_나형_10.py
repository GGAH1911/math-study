import sympy as sp
from sympy import symbols, limit, diff, solve

x, a, b = symbols('x a b', real=True)

# a = 3, b = 6 대입
a_val, b_val = 3, 6

# x < 1에서 함수
f1 = x**3 + a_val*x + b_val
f1_at_1_minus = f1.subs(x, 1)

# x >= 1에서 함수
f2 = b_val*x + 4
f2_at_1 = f2.subs(x, 1)

# 연속성 확인
continuous = (f1_at_1_minus == f2_at_1)

# 미분가능성 확인
f1_prime = diff(f1, x)
f2_prime = diff(f2, x)
f1_prime_at_1 = f1_prime.subs(x, 1)
f2_prime_at_1 = f2_prime.subs(x, 1)
differentiable = (f1_prime_at_1 == f2_prime_at_1)

# 최종 검증
if continuous and differentiable and f1_at_1_minus == f2_at_1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')