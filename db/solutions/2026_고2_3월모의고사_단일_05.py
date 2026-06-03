from sympy import symbols, Eq, solve

x = symbols('x')

# 원래 직선: y = (1/3)x - 1
# 기울기: 1/3
# 수직인 직선의 기울기: -3
# 점 (3, 1)을 지나는 직선: y = -3x + b

# 점 (3, 1)이 직선 위에 있는지 확인
# 1 = -3(3) + b
b = 1 + 3*3
print(f'y절편: {b}')

# y절편이 10인지 확인
if b == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')