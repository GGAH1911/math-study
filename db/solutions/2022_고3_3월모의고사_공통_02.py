from sympy import symbols, diff
x = symbols('x')
f = x**3 + 2*x**2 + 3*x + 4
f_prime = diff(f, x)
result = f_prime.subs(x, -1)
if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')