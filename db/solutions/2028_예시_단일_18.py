import sympy as sp
x = sp.Symbol('x')
f = x**3 - 2*x**2 + x
g = x**2 - x
limit1 = sp.limit((f - x) * (g - x) / x**3, x, 0)
limit2 = sp.limit((f + x) * (g + x) / x**3, x, 0)
f3 = f.subs(x, 3)
g8 = g.subs(x, 8)
result = f3 + g8
if result == 68 and limit1 == 4 and limit2 == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')