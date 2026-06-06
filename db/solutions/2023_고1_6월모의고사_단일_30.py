import sympy as sp
a = sp.Rational(3, 2)
f = lambda x: a * x**2
g = lambda x: -a * x**2 + 4*a*x - 8*a
result = f(22) + g(22)
if result == 120:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result}')