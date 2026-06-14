from sympy import symbols, expand, solve, diff
x = symbols('x')
f = 3*x**2 - 6*x - 24
f_prime = diff(f, x)
print(f'f(0) = {f.subs(x, 0)}')
print(f'f\'(2) = {f_prime.subs(x, 2)}')
print(f'lim f(x)/x^2 as x->inf = {3}')
roots = solve(f, x)
print(f'Roots: {roots}')
if f.subs(x, 0) == -24 and f_prime.subs(x, 2) == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')