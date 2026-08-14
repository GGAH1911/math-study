# f(x)=x^3+2x^2+x+2, 직선 y=4x+2. 교점을 실제로 풀어 P,Q,R 을 정하고 A-B 를 적분으로 계산.
import sympy as sp

x = sp.symbols('x', real=True)
f = x**3 + 2*x**2 + x + 2
g = 4*x + 2
xs = sorted(sp.solve(sp.Eq(f, g), x))               # -3, 0, 1
Qx = sp.Integer(0)                                   # y축 위 교점
Px = max(xs)                                         # 제1사분면 교점 → x=1
Rx = sp.solve(sp.Eq(g, 0), x)[0]                     # 직선의 x절편 -1/2
root = [r for r in sp.solve(f, x) if r.is_real][0]   # 곡선의 x절편 -2
A = sp.integrate(f, (x, root, Qx)) - sp.integrate(g, (x, Rx, Qx))
B = sp.integrate(g - f, (x, Qx, Px))
val = sp.simplify(A - B)
choices = {1: sp.Integer(2), 2: sp.Rational(9, 4), 3: sp.Rational(5, 2),
           4: sp.Rational(11, 4), 5: sp.Integer(3)}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [2] else 'VERIFY_FAIL')
