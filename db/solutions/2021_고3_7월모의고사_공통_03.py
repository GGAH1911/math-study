import sympy as sp
x, a = sp.symbols('x a')
f = x**2 - a*x
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 1)
print('f_prime(1) =', result)
if result.subs(a, 2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')