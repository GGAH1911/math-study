import sympy as sp
x = sp.symbols('x', positive=True)
# 원래 문제: 곡선 y = 2x*sqrt(x*sin(x^2))는 단면(반원)의 지름
y = 2*x*sp.sqrt(x*sp.sin(x**2))
radius = y/2
area = sp.Rational(1,2)*sp.pi*radius**2
V = sp.integrate(area, (x, sp.sqrt(sp.pi/6), sp.sqrt(sp.pi/2)))
V = sp.simplify(V)
candidate = (sp.sqrt(3)*sp.pi**2 + 6*sp.pi)/48
if sp.simplify(V - candidate) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', V, candidate)
