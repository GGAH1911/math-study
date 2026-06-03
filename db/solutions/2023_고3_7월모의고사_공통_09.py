import sympy as sp
x = sp.Symbol('x')
n = 3
eq = (x**n - 8) * (x**(2*n) - 8)
roots = sp.solve(eq, x)
real_roots = [r for r in roots if r.is_real]
product = sp.prod(real_roots)
result = 'VERIFY_PASS' if product == -4 else 'VERIFY_FAIL'
print(result)