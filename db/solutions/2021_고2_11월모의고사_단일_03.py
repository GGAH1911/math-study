from sympy import symbols, diff
x = symbols('x')
f = x**3 + 3*x + 1
f_prime = diff(f, x)
result = f_prime.subs(x, 1)
if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')