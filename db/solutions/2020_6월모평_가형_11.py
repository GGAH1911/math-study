import sympy as sp
x = sp.Symbol('x')
f = x * sp.exp(x)
f_prime = sp.diff(f, x)
f_double_prime = sp.diff(f_prime, x)
inflection_x = sp.solve(f_double_prime, x)
a = inflection_x[0]
b = f.subs(x, a)
product = a * b
product_simplified = sp.simplify(product)
expected = 4 / sp.exp(2)
if sp.simplify(product_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')