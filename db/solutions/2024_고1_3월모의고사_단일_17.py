import sympy as sp
a = sp.Rational(3, 5)
f = lambda x: a * x * (x - 4)
result = f(10)
print('VERIFY_PASS' if result == 36 else 'VERIFY_FAIL')