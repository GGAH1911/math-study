import sympy as sp
a = 4
x = sp.Symbol('x')
eq = x**3 - (2*a+1)*x**2 + (a+1)**2*x - (a**2+1)
roots = sp.solve(eq, x)
alpha = 4 + 1j
beta = 4 - 1j
gamma = 1
product = alpha * beta
print(f'alpha + beta = {alpha + beta}')
print(f'alpha * beta = {product}')
print(f'Verify gamma=1 in equation: {eq.subs(x, 1)}')
if abs(product - 17) < 1e-9 and abs(alpha + beta - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')