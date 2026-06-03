import sympy as sp
x = sp.Symbol('x')
P = lambda x_val: x_val**3 - x_val**2
result = P(4)
print('VERIFY_PASS' if result == 48 else 'VERIFY_FAIL')