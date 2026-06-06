import sympy as sp
x = sp.Symbol('x')
f = -(x-2)**2 + 15
result_at_4 = f.subs(x, 4)
print('VERIFY_PASS' if result_at_4 == 11 else 'VERIFY_FAIL')