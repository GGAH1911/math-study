import sympy as sp
x = sp.Symbol('x')
f_prime = 3*x**2 + 4*x + 5
f = sp.integrate(f_prime, x) + 4  # +4는 f(0)=4 조건
result = f.subs(x, 1)
print('VERIFY_PASS' if result == 12 else 'VERIFY_FAIL')