import sympy as sp
x = sp.Symbol('x')
m = 5
# 교점을 구하는 방정식
eq = x**2 + (1-m)*x + 4
roots = sp.solve(eq, x)
print(f'접점 x좌표: {roots}')
print(f'판별식: {(1-m)**2 - 16}')
if abs((1-m)**2 - 16) < 1e-10:
    x_touch = roots[0]
    y_parabola = x_touch**2 + x_touch
    y_line = m*x_touch - 4
    slope_parabola = 2*x_touch + 1
    slope_line = m
    if abs(y_parabola - y_line) < 1e-10 and abs(slope_parabola - slope_line) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')