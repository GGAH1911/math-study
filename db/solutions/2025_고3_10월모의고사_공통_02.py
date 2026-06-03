from sympy import symbols, limit, diff
x, h = symbols('x h')
f = x**3 + 2*x + 1
f_prime_def = (f.subs(x, 1+h) - f.subs(x, 1)) / h
result = limit(f_prime_def, h, 0)
f_prime = diff(f, x).subs(x, 1)
if result == 5 and f_prime == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')