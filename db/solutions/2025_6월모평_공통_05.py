import sympy as sp
x = sp.Symbol('x')
f = (x**2 - 1) * (x**2 + 2*x + 2)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 1)
if result == 10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')