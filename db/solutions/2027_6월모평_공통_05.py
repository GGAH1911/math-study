from sympy import symbols, diff, expand
x = symbols('x')
f = (3*x - 1) * (x**2 - 2*x + 2)
f_prime = diff(f, x)
result = f_prime.subs(x, 2)
print('VERIFY_PASS' if result == 16 else 'VERIFY_FAIL')