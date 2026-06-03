import sympy as sp
h = sp.Symbol('h')
avg_rate = h**2 + 2*h + 3
derivative_at_1 = sp.limit(avg_rate, h, 0)
print('VERIFY_PASS' if derivative_at_1 == 3 else 'VERIFY_FAIL')