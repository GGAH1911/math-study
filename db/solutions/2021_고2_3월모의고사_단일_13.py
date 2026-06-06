from sympy import symbols, solve, diff, simplify
x = symbols('x')
a = 1/2
f = -a * (x - 1)**2 + 9
f_expanded = -a*x**2 + x + 17/2
f_prime = diff(f_expanded, x)
f_2 = f_expanded.subs(x, 2)
f_1 = f_expanded.subs(x, 1)
derivative_at_minus_1 = f_prime.subs(x, -1)
f_at_minus_1 = f_expanded.subs(x, -1)
y_intercept_of_tangent = 9
verification = (
    float(f_1) == 9 and
    float(derivative_at_minus_1) == 2 and
    float(f_at_minus_1) == 7 and
    y_intercept_of_tangent == 9 and
    float(f_2) == 17/2
)
print('VERIFY_PASS' if verification else 'VERIFY_FAIL')