import sympy as sp
x, a = sp.symbols('x a')
f = (x + a) * sp.exp(x)
f_prime = sp.diff(f, x)
a_val = 5
result = f_prime.subs([(x, 2), (a, a_val)])
expected = 8 * sp.exp(2)
if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')