import sympy as sp
x = sp.Symbol('x')
f = sp.exp(x) * (2*sp.sin(x) + sp.cos(x))
f_prime = sp.diff(f, x)
f_prime_0 = f_prime.subs(x, 0)
answer = 3
if f_prime_0 == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')