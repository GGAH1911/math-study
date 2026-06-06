from sympy import symbols, solve, simplify
x, y = symbols('x y')
# 원래 주어진 조건
# 1. 점 (2, 5)를 지남
# 2. 직선 3x + 2y - 4 = 0에 수직
# 3. 방정식: 2x + ay + b = 0
a, b = -3, 11
# 조건 1: 점 (2, 5)가 2x + ay + b = 0을 만족
condition1 = 2*2 + a*5 + b
# 조건 2: 직선 3x + 2y - 4 = 0과 2x + ay + b = 0이 수직
# 수직 조건: A1*A2 + B1*B2 = 0
A1, B1 = 3, 2
A2, B2 = 2, a
vertical_check = A1*A2 + B1*B2
if condition1 == 0 and vertical_check == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')