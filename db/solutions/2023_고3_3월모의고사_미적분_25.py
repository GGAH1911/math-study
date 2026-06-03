import sympy as sp
from sympy import symbols, limit, oo

a1, d, n = symbols('a1 d n')

# 등차수열 공식
a_n = a1 + (n - 1) * d
a_2n = a1 + (2*n - 1) * d

# 주어진 극한
expr = (a_2n - 6*n) / (a_n + 5)
limit_expr = limit(expr, n, oo)

# d = -3일 때
limit_val_d3 = limit_expr.subs(d, -3)
print(f'd=-3일 때 극한값: {limit_val_d3}')

# 극한값이 4인지 확인
if limit_val_d3 == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')