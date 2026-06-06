from sympy import symbols, diff, solve, simplify

a_val = 9
b_val = 2
x = symbols('x')
f = x**3 - 6*x**2 + a_val*x + b_val
f_prime = diff(f, x)

# Check that x=3 is a critical point
if abs(f_prime.subs(x, 3)) < 1e-10:
    critical_points = solve(f_prime, x)
    f_vals = [f.subs(x, cp) for cp in critical_points]
    sum_extrema = sum(f_vals)
    
    if abs(sum_extrema - 8) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')