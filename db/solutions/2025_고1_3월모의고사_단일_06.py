# 연립방정식 검증
from sympy import symbols, Eq, solve

x, y = symbols('x y')
eq1 = Eq(x + 2*y, 1)
eq2 = Eq(2*x - 3*y, 9)

solution = solve((eq1, eq2), (x, y))
a = solution[x]
b = solution[y]

result = a + b

if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')