from sympy import symbols, solve, simplify

# 정의
a = symbols('a', real=True)

# 내분점 공식: AB를 2:1로 내분
# P = ((1*2 + 2*5)/3, (1*a + 2*(-2))/3, (1*(-2) + 2*1)/3)
P_x = (1*2 + 2*5) / 3
P_y = (1*a + 2*(-2)) / 3
P_z = (1*(-2) + 2*1) / 3

# x축 위에 있으므로 y=0, z=0
# z=0은 자동 만족 (0/3=0)
# y=0 조건
eq = P_y
sol = solve(eq, a)
print(f'a = {sol[0]}')

# 검증: a=4일 때 내분점이 x축 위에 있는지 확인
a_val = 4
P_y_check = (1*a_val + 2*(-2)) / 3
P_z_check = (1*(-2) + 2*1) / 3

if P_y_check == 0 and P_z_check == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')