import sympy as sp

total = 0
for n in range(1, 5):
    x = sp.Symbol('x')
    eq = x**2 - (n+1)*x - n*(2*n+1)
    roots = sp.solve(eq, x)
    x1, x2 = sorted(roots)
    
    y1 = x1 + n
    y2 = x2 + n
    
    area = sp.Rational(1, 2) * sp.Abs(x1*y2 - x2*y1)
    area_simplified = sp.simplify(area)
    total += area_simplified

total = sp.simplify(total)
if total == 50:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')