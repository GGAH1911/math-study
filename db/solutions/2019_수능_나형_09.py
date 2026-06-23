from sympy import symbols, diff, solve, simplify
x, a = symbols('x a')
f = x**3 - 3*x + a
f_prime = diff(f, x)
critical_pts = solve(f_prime, x)
f_double_prime = diff(f_prime, x)
max_pt = -1
if f_double_prime.subs(x, max_pt) < 0:
    max_val = f.subs(x, max_pt)
    a_val = solve(max_val - 7, a)[0]
    f_check = x**3 - 3*x + a_val
    if abs(f_check.subs(x, max_pt) - 7) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')