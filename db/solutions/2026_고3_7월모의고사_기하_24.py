from sympy import symbols, solve, Eq

a = symbols('a', real=True)

# 점 (a, 4)가 포물선 y^2 = 4(x-3) 위에 있음
eq = Eq(4**2, 4*(a-3))
a_val = solve(eq, a)[0]
print(f'a = {a_val}')  # a = 7

# 포물선 y^2 = 4(x-3)에서 준선은 x = 2 (h - p = 3 - 1)
directrix_x = 2
point_x = a_val

# 점 (7, 4)에서 준선 x=2까지의 거리
distance = abs(point_x - directrix_x)
print(f'Distance = {distance}')  # 5

# 검증: 점이 포물선 위에 있는지 확인
verify = 4**2 == 4*(a_val - 3)
print(f'Point on parabola: {verify}')

# 답
if distance == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')