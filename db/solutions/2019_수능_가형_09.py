import sympy as sp
x = sp.Symbol('x', real=True)
f = 1 / (1 + sp.exp(-x))
f_prime = sp.diff(f, x)
f_prime_at_minus_1 = f_prime.subs(x, -1)
g_prime_f_minus_1 = 1 / f_prime_at_minus_1
answer = sp.simplify(g_prime_f_minus_1)
expected = (1 + sp.E)**2 / sp.E
if sp.simplify(answer - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')