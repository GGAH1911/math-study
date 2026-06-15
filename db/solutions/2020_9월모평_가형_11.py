from sympy import symbols, exp, diff, solve
x = symbols('x')
f = (x**2 - 3) * exp(-x)
f_prime = diff(f, x)
critical = solve(f_prime, x)
print(f'Critical points: {critical}')
a = f.subs(x, 3)
b = f.subs(x, -1)
product = a * b
print(f'a = {a}')
print(f'b = {b}')
print(f'a*b = {product}')
from sympy import simplify, nsimplify
product_simplified = simplify(product)
print(f'Simplified: {product_simplified}')
if simplify(product_simplified + 12/exp(2)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')