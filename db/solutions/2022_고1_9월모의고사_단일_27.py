import sympy as sp
from sympy import symbols, expand, solve, factor

a = symbols('a')
x = symbols('x')

# 원래 방정식
eq = x**4 + (2*a+1)*x**3 + (3*a+2)*x**2 + (a+2)*x

# 검증할 a 값들
a_values = [-2, -1, 2, 3]
distinct_root_counts = []

for a_val in a_values:
    eq_sub = eq.subs(a, a_val)
    roots = solve(eq_sub, x)
    distinct_roots = set(roots)
    distinct_root_counts.append(len(distinct_roots))

# 모든 a 값에서 서로 다른 실근의 개수가 3이어야 함
if all(count == 3 for count in distinct_root_counts):
    product = 1
    for val in a_values:
        product *= val
    if product == 12:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')