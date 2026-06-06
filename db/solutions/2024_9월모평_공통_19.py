from sympy import symbols, integrate, solve
x = symbols('x')
f1 = 3*x**3 - 7*x**2
f2 = -x**2
intersections = solve(f1 - f2, x)
assert intersections == [0, 2], f'교점 오류: {intersections}'
area = integrate(f2 - f1, (x, 0, 2))
if area == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')