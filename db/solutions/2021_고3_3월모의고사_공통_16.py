from sympy import symbols, diff, simplify
x = symbols('x')
f = 2*x**2 + 5*x + 3
g = x**3 + 2
h = f * g
h_prime = diff(h, x)
result = h_prime.subs(x, 0)
print('VERIFY_PASS' if result == 10 else 'VERIFY_FAIL')