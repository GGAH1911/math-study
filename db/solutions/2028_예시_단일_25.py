import sympy as sp
x = sp.Symbol('x')
f = x**3 + 3*x**2 + 5
f_prime = sp.diff(f, x)
f_double_prime = sp.diff(f_prime, x)
critical_points = sp.solve(f_prime, x)
print('Critical points:', critical_points)
for cp in critical_points:
    second_deriv_val = f_double_prime.subs(x, cp)
    if second_deriv_val < 0:
        extremum_type = 'max'
    else:
        extremum_type = 'min'
    print(f'x = {cp}: {extremum_type}, f({cp}) = {f.subs(x, cp)}')
result = f.subs(x, 3)
print(f'f(3) = {result}')
if result == 59:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')