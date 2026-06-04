import sympy as sp
x, y = sp.symbols('x y', real=True, positive=False)
F = 2*x + sp.sqrt(y) - x*y
# (-1, 1)이 곡선 위에 있는지 확인
on_curve = sp.simplify(F.subs({x: -1, y: 1}))
if on_curve != 0:
    print('VERIFY_FAIL')
else:
    F_x = sp.diff(F, x)
    F_y = sp.diff(F, y)
    slope = sp.simplify(-F_x / F_y)
    slope_val = sp.simplify(slope.subs({x: -1, y: 1}))
    if slope_val == sp.Rational(-2, 3):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
