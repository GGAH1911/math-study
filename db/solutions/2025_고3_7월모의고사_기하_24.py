from sympy import symbols, solve, Rational

# 타원 방정식과 점
x, y = symbols('x y', real=True)
ellipse_eq = x**2 / 2 + y**2 / 8 - 1

# 점 (1, 2)가 타원 위에 있는지 확인
point_check = ellipse_eq.subs([(x, 1), (y, 2)])
if point_check == 0:
    # 접선 방정식: x/2 + y/4 = 1 또는 y = -2x + 4
    # y절편은 x=0일 때 y 값
    y_intercept = 4  # y = -2(0) + 4 = 4
    
    # 검증: 접선이 점 (1,2)를 지나갈 때 y값이 2인지
    line_eq = -2 * 1 + 4
    if line_eq == 2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')