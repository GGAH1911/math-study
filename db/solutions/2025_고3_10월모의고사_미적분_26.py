from sympy import *
x = symbols('x', positive=True)
y = 2*sqrt(x)*exp(-x**2)
A = y**2  # 4*x*exp(-2*x**2)
V = integrate(A, (x, Rational(1,2), 1))
expected = exp(Rational(-1,2)) - exp(-2)
diff = simplify(V - expected)
if diff == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: V={V}, expected={expected}')