import sympy as sp
x = sp.Symbol('x')
f_prime = 3*x**2 + 4*x
f = sp.integrate(f_prime, x) + 3  # 부정적분에 C=3
result = f.subs(x, 1)
print('VERIFY_PASS' if result == 6 else 'VERIFY_FAIL')