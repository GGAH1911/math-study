import sympy as sp

x = sp.Symbol('x')
a_val = 6

# 원래 첫 번째 곡선
f = x**3 - 4*x + 5
# 점 (1,2) 검증
assert f.subs(x, 1) == 2, 'point not on curve'

# 접선 기울기
df = sp.diff(f, x)
slope = df.subs(x, 1)  # -1

# 접선 방정식: y = slope*x + (2 - slope*1)
tangent = sp.Lambda(x, slope*x + (2 - slope*1))

# 두 번째 곡선
g = x**4 + 3*x + a_val
dg = sp.diff(g, x)

# 접점 t에서 기울기 같아야 함
t = sp.Symbol('t')
tangent_points = sp.solve(dg.subs(x, t) - slope, t)

passed = False
for tp in tangent_points:
    y_line = tangent(tp)
    y_curve = g.subs(x, tp)
    if sp.simplify(y_line - y_curve) == 0:
        passed = True
        break

if passed:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
