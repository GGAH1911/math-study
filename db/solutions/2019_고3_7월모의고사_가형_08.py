from sympy import *
x, y = symbols('x y', real=True)
# 곡선 방정식: xy - y^3*ln(x) = 2
curve = x*y - y**3*ln(x) - 2
# x=1, y=2에서 확인
verify_point = curve.subs([(x, 1), (y, 2)])
if verify_point == 0:
    # 음함수 미분으로 dy/dx 계산
    dy_dx = -diff(curve, x) / diff(curve, y)
    result = dy_dx.subs([(x, 1), (y, 2)])
    if simplify(result - 6) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')