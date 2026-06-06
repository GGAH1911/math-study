from sympy import *
x = symbols('x')
f = -x**4/4 + 3*x + 8
f_prime = diff(f, x)
print('f\'(x) =', f_prime)
print('f(2) =', f.subs(x, 2))
print('f(0) =', f.subs(x, 0))
assert f_prime == -x**3 + 3
assert f.subs(x, 2) == 10
assert f.subs(x, 0) == 8
print('VERIFY_PASS')