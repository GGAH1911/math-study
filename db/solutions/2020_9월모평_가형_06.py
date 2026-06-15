import sympy as sp
y_val = sp.pi / 2
sin_y = sp.sin(y_val)
cos_y = sp.cos(y_val)
x_val = 0

# 곡선이 주어진 점을 지나는지 확인
curve_check = sp.pi * x_val - (cos_y + x_val * sin_y)
if curve_check == 0:
    # 암시적 미분으로 구한 기울기
    numerator = sp.pi - sin_y
    denominator = x_val * cos_y - sin_y
    slope = numerator / denominator
    slope_simplified = sp.simplify(slope)
    
    # 정답과 비교
    expected = 1 - sp.pi
    if sp.simplify(slope_simplified - expected) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')