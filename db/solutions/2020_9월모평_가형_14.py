from sympy import *
x = symbols('x', real=True, positive=True)
k_val = Rational(1, 4)
f_squared = 4*x*exp(x**2/2)
area = sqrt(3)*x*exp(x**2/2)
x1, x2 = sqrt(2), 2
volume = integrate(area, (x, x1, x2))
expected = sqrt(3)*(exp(2) - exp(1))
if simplify(volume - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')