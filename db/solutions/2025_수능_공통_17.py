from sympy import symbols, integrate, diff
x = symbols('x')
f_prime = 9*x**2 + 4*x
f = integrate(f_prime, x)
C = 6 - f.subs(x, 1)
f = f + C
result = f.subs(x, 2)
if result == 33:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')