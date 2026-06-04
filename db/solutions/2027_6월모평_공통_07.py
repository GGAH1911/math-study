from sympy import symbols, diff, solve
x = symbols('x')
f = x**3 - 3*x + 9
f_prime = diff(f, x)
critical_points = solve(f_prime, x)
min_value = f.subs(x, 1)
print('VERIFY_PASS' if min_value == 7 else 'VERIFY_FAIL')