from sympy import symbols, diff
x = symbols('x')
f = x**4 + 3*x - 2
f_prime = diff(f, x)
result = f_prime.subs(x, 2)
if result == 35:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')