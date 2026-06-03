import sympy as sp
from sympy import symbols, tan, exp, limit, oo

x = symbols('x', real=True)

# 원래 문제의 극한식
f = tan(5*x) / (exp(x) - 1)

# x -> 0에서의 극한값 계산
limit_value = limit(f, x, 0)

print(f'Limit value: {limit_value}')
if limit_value == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')