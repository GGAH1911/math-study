import sympy as sp
x, a = sp.symbols('x a')
f = 2*x**2 + a*x + 3
f_prime = sp.diff(f, x)
f_prime_at_2 = f_prime.subs(x, 2)
eq = sp.Eq(f_prime_at_2, 18)
a_value = sp.solve(eq, a)[0]
if a_value == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')