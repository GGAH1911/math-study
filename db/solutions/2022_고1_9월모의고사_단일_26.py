import sympy as sp
from sympy import sqrt, symbols, solve

# 점들 정의
A1 = (3, sqrt(91))
A2 = (7, sqrt(51))
B = (-10, 0)

# A1B의 기울기
m1 = (A1[1] - B[1]) / (A1[0] - B[0])

# A1B에 수직인 직선: B를 지나고 기울기가 -1/m1
x = symbols('x')
y1 = -(1/m1) * (x - B[0])

# 원과의 교점
circle_eq = x**2 + y1**2 - 100
x_solutions = solve(circle_eq, x)
C1_x = [sol for sol in x_solutions if sol != -10][0]
C1_y = -(1/m1) * (C1_x - B[0])

# A2B의 기울기
m2 = (A2[1] - B[1]) / (A2[0] - B[0])

# A2B에 수직인 직선
y2 = -(1/m2) * (x - B[0])
circle_eq2 = x**2 + y2**2 - 100
x_solutions2 = solve(circle_eq2, x)
C2_x = [sol for sol in x_solutions2 if sol != -10][0]

# 답 검증
a = C1_y
b = C2_x
answer = a**2 + b**2
answer_simplified = sp.simplify(answer)

if answer_simplified == 140:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')