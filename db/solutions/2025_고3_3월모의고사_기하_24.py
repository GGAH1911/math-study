from sympy import symbols, simplify, Rational, sqrt

a_val = 6
# 원래 식: x^2/a^2 - y^2/4 = 1
# 점근선은 x^2/a^2 - y^2/4 = 0 => y = ±(2/a) x
# 주어진 점근선 y = (1/3) x 이 점근선 중 하나와 같아야 함
slope_given = Rational(1, 3)
slope_asymp = Rational(2, a_val)
if a_val > 0 and simplify(slope_asymp - slope_given) == 0:
    # 점근선 위 임의의 점 (3,1)이 hyperbola 식에서 좌변 -> 0 인지 확인 (점근적 거동)
    x_t, y_t = 3, 1  # y = x/3 위의 점
    val = Rational(x_t,1)**2/Rational(a_val,1)**2 - Rational(y_t,1)**2/4
    # 점근선 위 점에서 좌변은 0 이어야 (점근선 식 x^2/a^2 - y^2/4 = 0)
    if val == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
