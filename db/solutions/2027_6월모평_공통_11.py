import sympy as sp
x = sp.Symbol('x')
m, n = 3, -6
f = lambda t: m*t + n
result = f(4)
print('VERIFY_PASS' if result == 6 else 'VERIFY_FAIL')