from sympy import symbols, integrate, Abs
x = symbols('x')
f = x**3 - 2*x**2
area = Abs(integrate(f, (x, 0, 2)))
result = float(area)
expected = 4/3
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')