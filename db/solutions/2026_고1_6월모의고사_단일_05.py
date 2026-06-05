import sympy as sp
from sympy import symbols, solve

x = symbols('x')

# 원래 문제의 조건
cond1 = x**2 - 3*x + 5 <= x + 5
cond2 = x + 5 <= 8

# 각 부등식을 풀기
sol1 = solve(x**2 - 3*x + 5 <= x + 5, x)
sol2 = solve(x + 5 <= 8, x)

# 정수 해 찾기
valid_integers = []
for xi in range(-10, 15):
    lhs1 = xi**2 - 3*xi + 5
    mid = xi + 5
    rhs = 8
    if lhs1 <= mid <= rhs:
        valid_integers.append(xi)

# 검증: 답이 4개인지 확인
if len(valid_integers) == 4 and valid_integers == [0, 1, 2, 3]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')