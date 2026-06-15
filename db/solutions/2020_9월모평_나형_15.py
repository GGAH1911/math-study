import sympy as sp
x = sp.Symbol('x')
f = x**2 - 2*x
g = -(f.subs(x, x-1)) - 1
g_expanded = sp.expand(g)
eq = sp.solve(f - g_expanded, x)
print(f'교점: {eq}')
integrand = g_expanded - f
integrand_simplified = sp.expand(integrand)
area = sp.integrate(integrand_simplified, (x, eq[0], eq[1]))
print(f'넓이: {area}')
if area == sp.Rational(1, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')