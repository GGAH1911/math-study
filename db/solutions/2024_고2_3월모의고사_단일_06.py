from sympy import symbols, solve, simplify
a = symbols('a')
# 최종 원의 방정식: (x+5)^2 + (y-10)^2 = 25
# 점 (0, a)를 대입
equation = (0 + 5)**2 + (a - 10)**2 - 25
solution = solve(equation, a)
print(solution)
assert 10 in solution, f'Expected a=10, got {solution}'
# 검증: 점 (0, 10)이 원 위에 있는지 확인
verify = (0 + 5)**2 + (10 - 10)**2
assert verify == 25, f'Point (0, 10) should satisfy the circle equation'
print('VERIFY_PASS')