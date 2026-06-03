from sympy import symbols, solve

# 원래 문제 조건
side = 2  # 정사각형 밑면 한 변의 길이
volume = 12  # 주어진 부피

h = symbols('h', positive=True)
# 부피 방정식: side^2 * h = volume
h_val = solve(side**2 * h - volume, h)[0]  # h = 3

# 겉넓이 계산
surface_area = 2 * (side * side) + 4 * (side * h_val)

# 검증: 답이 32인지 확인
if surface_area == 32:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: surface_area={surface_area}')
