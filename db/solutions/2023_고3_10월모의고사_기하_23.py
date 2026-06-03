from sympy import symbols, solve, simplify
a = symbols('a')
# 외분점의 x좌표
x_coord = (3*2 - 2*a) / (3-2)
# yz 평면 위의 조건: x = 0
eq = x_coord
solution = solve(eq, a)
print(f'a = {solution[0]}')
assert solution[0] == 3, 'VERIFY_FAIL'
print('VERIFY_PASS')