from sympy import symbols, solve, simplify

k = 4
x = symbols('x')

eq = (x**2 + k*x + 2) * (x**2 + k*x + 6) + 3
roots = solve(eq, x)

real_count = sum(1 for r in roots if r.is_real)
complex_count = len(roots) - real_count

for root in roots:
    result = simplify(eq.subs(x, root))
    if result != 0:
        print('VERIFY_FAIL')
        exit()

if real_count == 2 and complex_count == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')