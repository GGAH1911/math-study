from sympy import symbols, integrate, Rational
x, k = symbols('x k', real=True)
f = x**2 - 5*x
g = x
# intersection
A_total = integrate(g - f, (x, 0, 6))
k_val = 3
A_left = integrate(g - f, (x, 0, k_val))
A_right = integrate(g - f, (x, k_val, 6))
if A_left == A_right == A_total/2 == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
