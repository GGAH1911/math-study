from sympy import symbols, integrate, solve
x = symbols('x')
f = 3*x**2 - x  # 원래 곡선
g = 5*x         # 원래 직선
pts = solve(f - g, x)
a, b = min(pts), max(pts)
area = integrate(g - f, (x, a, b))
print('VERIFY_PASS' if area == 4 else f'VERIFY_FAIL area={area}')