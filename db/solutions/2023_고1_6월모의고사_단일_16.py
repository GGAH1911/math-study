from sympy import symbols, expand, factor, solve
x, a = symbols('x a')
eq = (x - a) * (x**2 + (1 - 3*a)*x + 4)
a_val = 2
eq_sub = eq.subs(a, a_val)
roots = solve(eq_sub, x)
print(f'roots: {roots}')
alpha, beta = 2, 4
product = alpha * beta
print(f'alpha*beta = {product}')
if product == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')