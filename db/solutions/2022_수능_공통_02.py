from sympy import symbols, diff

x = symbols('x')
f = x**3 + 3*x**2 + x - 1
f_prime = diff(f, x)
result = f_prime.subs(x, 1)

if result == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')