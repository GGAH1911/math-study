from sympy import symbols, diff
x = symbols('x')
f = (x - 1) * (x**3 + x**2 + 5)
f_prime = diff(f, x)
result = f_prime.subs(x, 1)
if result == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')