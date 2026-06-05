import sympy as sp
from sympy import log, sqrt, symbols

# k = 32일 때 검증
k = 32

# 이차방정식: x^2 - (log_2(k) + 10)x + 5 = 0
# 근과 계수의 관계
sum_roots = log(k, 2) + 10  # p + q
product_roots = 5  # pq

# 근의 공식으로 실제 근 계산
x = symbols('x')
equation = x**2 - (log(k, 2) + 10)*x + 5
roots = sp.solve(equation, x)
p, q = roots[0], roots[1]

# 조건 검증: 1/p + 1/q = 3
condition_value = 1/p + 1/q
condition_simplified = sp.simplify(condition_value)

if sp.simplify(condition_simplified - 3) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')