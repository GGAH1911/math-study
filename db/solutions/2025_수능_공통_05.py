from sympy import symbols, diff
x = symbols('x')
f = (x**2 + 1) * (3*x**2 - x)
f_prime = diff(f, x)
result = f_prime.subs(x, 1)
if result == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')