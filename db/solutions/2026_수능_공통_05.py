from sympy import symbols, expand, diff
x = symbols('x')
f = (x+2)*(2*x**2 - x - 2)
f_prime = diff(f, x)
result = f_prime.subs(x, 1)
print('VERIFY_PASS' if result == 8 else f'VERIFY_FAIL: got {result}')