import sympy as sp

x = sp.Symbol('x')
f = (x**2 - 2*x - 7) * sp.exp(x)
f_prime = sp.diff(f, x)
f_prime_simplified = sp.factor(f_prime)

# Critical points
cpts = sp.solve(f_prime_simplified, x)

# Classify: x=-3 local max, x=3 local min
a = f.subs(x, -3)  # local max value
b = f.subs(x, 3)   # local min value

product = sp.simplify(a * b)

if product == -32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', product)
