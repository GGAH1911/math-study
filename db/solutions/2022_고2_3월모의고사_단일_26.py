from sympy import symbols, solve, simplify, Rational

a = symbols('a', real=True)

# Define the function
def f(x):
    return x**2 - 4*x + 3

# When a >= 2, b = f(a)
b_expr = f(a)

# a - b expression
a_minus_b = a - b_expr
a_minus_b_simplified = simplify(a_minus_b)

# Find critical point
derivative = a_minus_b_simplified.diff(a)
critical_points = solve(derivative, a)

print('Critical point:', critical_points)
a_opt = critical_points[0]
print('Optimal a:', a_opt)

# Calculate maximum value
max_value = a_minus_b_simplified.subs(a, a_opt)
max_value_simplified = simplify(max_value)
print('Maximum value (a - b):', max_value_simplified)

# Verify it equals 13/4
if max_value_simplified == Rational(13, 4):
    print('p = 4, q = 13')
    print('p + q =', 4 + 13)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')