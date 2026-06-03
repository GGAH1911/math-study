from sympy import symbols, diff, solve
x, k = symbols('x k')
f = x**3 - 3*x**2 + k
f_prime = diff(f, x)
critical_points = solve(f_prime, x)
max_point = 0
f_at_max = f.subs(x, max_point)
k_val = 9
f_sub = f.subs(k, k_val)
min_val = f_sub.subs(x, 2)
if min_val == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')