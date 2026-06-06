import sympy as sp
from sympy import symbols, solve, simplify

a = 4
x = symbols('x')
eq = x**2 - a*x - 4

# 방정식의 근 구하기
roots = solve(eq, x)
alpha, beta = roots[0], roots[1]

# 주어진 조건 검증
result = alpha/beta + beta/alpha
result_simplified = simplify(result)

if result_simplified == -6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result_simplified}')