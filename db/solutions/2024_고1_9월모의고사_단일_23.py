from sympy import symbols, solve, sympify

x = symbols('x', integer=True)

# 원래 부등식 조건
cond1 = 2*x <= x + 11  # x <= 11
cond2 = x + 5 < 4*x - 2  # x > 7/3

# 연립해를 찾기
solutions = []
for val in range(-10, 20):
    check1 = 2*val <= val + 11
    check2 = val + 5 < 4*val - 2
    if check1 and check2:
        solutions.append(val)

print(f'Solutions: {solutions}')
print(f'Count: {len(solutions)}')
if len(solutions) == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')