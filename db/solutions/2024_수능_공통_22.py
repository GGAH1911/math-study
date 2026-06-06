import sympy as sp
x = sp.Symbol('x')
f = x**3 - 3*x**2/8 - 5*x/8
result = f.subs(x, 8)
print(f'f(8) = {result}')
if result == 483:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')