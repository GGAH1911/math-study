import sympy as sp
x, a = sp.symbols('x a')
f = x**2 + a*x
f_prime = sp.diff(f, x)
f_prime_at_1 = f_prime.subs(x, 1)
eq = sp.Eq(f_prime_at_1, 4)
a_value = sp.solve(eq, a)[0]
if a_value == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')