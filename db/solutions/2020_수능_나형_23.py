from sympy import symbols, solve, simplify

CANDIDATE = 36

# 등비수열 조건
r = symbols('r', positive=True, real=True)

# 주어진 조건: r^2 + r = 12
equation = r**2 + r - 12
solutions = solve(equation, r)

# 양수 해 찾기
r_value = [sol for sol in solutions if sol > 0][0]

# 구하는 값 계산
answer_calc = r_value**2 + r_value**3
answer_simplified = simplify(answer_calc)

# 검증
if answer_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')