import sympy as sp
x = sp.Symbol('x')
a = 2
b = 2
# 원래 방정식: x^2 - 3x + a = 0
equation = x**2 - 3*x + a
roots = sp.solve(equation, x)
print(f'근: {roots}')
if set(roots) == {1, b}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')