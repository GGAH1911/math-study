# f(x^3+2x+2)=3-sin(πx) 를 미분: f'(x^3+2x+2)(3x^2+2) = -π cos(πx).
# x=1 이면 인수 x^3+2x+2 = 5 이므로 f'(5) 를 실제로 푼다.
import sympy as sp

x = sp.symbols('x', real=True)
g = x**3 + 2*x + 2
assert sp.simplify(g.subs(x, 1) - 5) == 0       # x=1 에서 안쪽 값이 5
fp = sp.symbols('fp')                            # f'(5)
eq = sp.Eq(fp * sp.diff(g, x).subs(x, 1), sp.diff(3 - sp.sin(sp.pi*x), x).subs(x, 1))
val = sp.simplify(sp.solve(eq, fp)[0])
choices = {1: sp.pi/10, 2: sp.pi/5, 3: 3*sp.pi/10, 4: 2*sp.pi/5, 5: sp.pi/2}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [2] else 'VERIFY_FAIL')
