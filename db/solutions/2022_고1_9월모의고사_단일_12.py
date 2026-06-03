from sympy import symbols, solve
x = symbols('x')
a, b = -2, 1
first_fn = x**2 + a*x + b
second_fn = x**2 + b*x + a
roots = solve(second_fn, x)
distance = abs(roots[1] - roots[0])
if distance == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')