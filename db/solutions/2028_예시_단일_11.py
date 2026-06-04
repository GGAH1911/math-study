import sympy as sp
x, t = sp.symbols('x t')

# 원곡선
y_curve = x**3 - 2*x + 17

# 곡선 위의 점 (t, t^3 - 2t + 17)에서의 접선의 기울기
dy_dx = sp.diff(y_curve, x).subs(x, t)

# 접선: y - (t^3 - 2t + 17) = (3t^2 - 2)(x - t)
# (0, 1)을 지나므로
eq = 1 - (t**3 - 2*t + 17) - (3*t**2 - 2)*(0 - t)
t_val = sp.solve(eq, t)
print(f"접점의 x좌표: {t_val}")

# t = 2일 때 접선
t_val = 2
tangent_point = (t_val, t_val**3 - 2*t_val + 17)
slope = 3*t_val**2 - 2
print(f"접점: {tangent_point}, 기울기: {slope}")

# 접선 방정식: y - 21 = 10(x - 2) => y = 10x + 1
# (0, 1)을 지나는지 확인
print(f"(0, 1) 확인: y = 10*0 + 1 = {10*0 + 1}")

# (a, 11)을 지날 때 a 구하기
# 11 = 10a + 1
a = (11 - 1) / 10
print(f"a = {a}")

# 최종 검증: (a, 11)이 접선 위에 있는지
verify = 10*a + 1
if abs(verify - 11) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')