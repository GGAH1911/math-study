import sympy as sp
x = sp.Symbol('x')
f = (x+1)*(2*x**2-5*x+1)
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')