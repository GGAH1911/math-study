from sympy import symbols, solve, simplify

a1, r = symbols('a1 r', positive=True, real=True)

# 조건: a3 = 4*a1 + 3*a2
# a1*r^2 = 4*a1 + 3*a1*r
eq = a1*r**2 - 4*a1 - 3*a1*r

# a1 > 0이므로 r에 대한 방정식
equation = r**2 - 3*r - 4
solutions = solve(equation, r)

# 양수 해 찾기
positive_r = [sol for sol in solutions if sol > 0][0]

# a6/a4 계산
result = positive_r**2

if result == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')