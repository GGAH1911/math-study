from sympy import symbols, solve, diff
x, k = symbols('x k')
curve = 2*x**4 - 4*x + k
line = 4*x + 5
curve_derivative = diff(curve, x)
line_slope = 4
tangent_x = solve(curve_derivative - line_slope, x)
tangent_x = [val for val in tangent_x if val.is_real][0]
k_value = 11
curve_y_at_tangent = (2*tangent_x**4 - 4*tangent_x + k_value).subs(x, 1)
line_y_at_tangent = (4*tangent_x + 5).subs(x, 1)
if abs(float(curve_y_at_tangent) - float(line_y_at_tangent)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')