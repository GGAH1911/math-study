import sympy as sp
x, a = sp.symbols('x a')
f = x**3 + 3*x**2 - 9*x + 4
f_prime = sp.diff(f, x)
print('f(1) derivative:', f_prime.subs(x, 1))
print('f(-3) value:', f.subs(x, -3))
print('Critical points:', sp.solve(f_prime, x))
if f.subs(x, -3) == 31 and f_prime.subs(x, 1) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')