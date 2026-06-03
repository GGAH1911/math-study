import sympy as sp
x, y = sp.symbols('x y', positive=True, real=True)

# 조건 1: xy = 5
eq1 = x*y - 5

# 조건 2: x + y = sqrt(21)
eq2 = x + y - sp.sqrt(21)

# 조건 3: 코사인 법칙 검증
# sin(angle) = 4/5, cos(angle) = -3/5
# 17 = x^2 + y^2 - 2xy*cos(angle)
sin_angle = sp.Rational(4, 5)
cos_angle = sp.Rational(-3, 5)

# 넓이 조건: xy*sin(angle) = 4
area_check = x*y*sin_angle - 4

# 코사인 법칙
law_of_cosines = x**2 + y**2 - 2*x*y*cos_angle - 17

# 해 구하기
sol = sp.solve([eq1, eq2], [x, y])

if sol:
    x_val, y_val = sol[0] if sol[0][0] > sol[0][1] else sol[1]
    
    # 검증
    area_result = float(x_val*y_val*sin_angle)
    cosine_result = float(x_val**2 + y_val**2 - 2*x_val*y_val*cos_angle)
    sum_result = float(x_val + y_val)
    
    if abs(area_result - 4) < 1e-9 and abs(cosine_result - 17) < 1e-9 and abs(sum_result - float(sp.sqrt(21))) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')