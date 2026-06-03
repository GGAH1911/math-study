import sympy as sp
x, y = sp.symbols('x y', real=True)
e = sp.E

# 곡선 방정식
curve = x**2 - y*sp.ln(x) + x - e

# 점 (e, e^2)이 곡선 위에 있는지 확인
check_point = curve.subs([(x, e), (y, e**2)])
print(f'Point on curve: {sp.simplify(check_point) == 0}')

# 암시함수 미분으로 dy/dx 구하기
# F(x,y) = x^2 - y*ln(x) + x - e = 0
# dy/dx = -F_x / F_y
F = x**2 - y*sp.ln(x) + x - e
F_x = sp.diff(F, x)
F_y = sp.diff(F, y)

dy_dx = -F_x / F_y

# (e, e^2)에서의 기울기
slope = dy_dx.subs([(x, e), (y, e**2)])
slope_simplified = sp.simplify(slope)

if sp.simplify(slope_simplified - (e + 1)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')