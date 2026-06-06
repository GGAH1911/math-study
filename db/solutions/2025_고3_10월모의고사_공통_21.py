import sympy as sp
x = sp.Symbol('x')
f = x**4 - 16*x**2 + 81
result = f.subs(x, 4)
print('f(4) =', result)
print('VERIFY_PASS' if result == 81 else 'VERIFY_FAIL')