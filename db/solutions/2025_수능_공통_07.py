from sympy import symbols, integrate, diff

x, t = symbols('x t')
integrand = 9*t**2 + 2
result = integrate(integrand, (t, 0, x))
target = 3*x**3 + 2*x

if result - target == 0:
    f_1 = 9*(1)**2 + 2
    if f_1 == 11:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')