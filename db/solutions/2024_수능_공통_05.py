from sympy import symbols, diff, integrate
x = symbols('x')
f_prime = 3*x*(x-2)
f = integrate(f_prime, x)
C = 6 - f.subs(x, 1)
f_complete = f + C
result = f_complete.subs(x, 2)
if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')