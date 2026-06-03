from sympy import symbols, simplify
x = symbols('x')
# 원래 문제의 직선 3x + 2y - 5 = 0과 평행하므로 기울기 -3/2
# 점 (2, 3)을 지나는 직선: y = -3/2 * x + b
# (2, 3)을 지나므로: 3 = -3/2 * 2 + b
b = 3 + 3/2 * 2
print(f'y절편: {b}')
# 검증: 구한 직선 y = -3/2 * x + 6이 점 (2, 3)을 지나는지 확인
y_at_2 = -3/2 * 2 + b
if abs(y_at_2 - 3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')