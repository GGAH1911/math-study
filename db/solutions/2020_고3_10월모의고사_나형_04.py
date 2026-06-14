import sympy as sp
from sympy import symbols, diff, limit, simplify

CANDIDATE = 6

# 조건: f'(2) = 3을 만족하는 함수 예시
# f(x) = 3x + c 형태의 1차 함수를 사용
# f'(x) = 3이므로 f'(2) = 3 만족

x, h, c = symbols('x h c')
f = lambda x_val: 3*x_val + c

# 주어진 조건 확인: lim_{x->2} (f(x)-f(2))/(x-2) = 3
numerator_cond = f(x) - f(2)
denominator_cond = x - 2
limit_cond = limit(numerator_cond / denominator_cond, x, 2)

# 구하려는 극한: lim_{h->0} (f(2+h) - f(2-h))/h
numerator_target = f(2+h) - f(2-h)
denominator_target = h
limit_target = limit(numerator_target / denominator_target, h, 0)

if limit_target == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')