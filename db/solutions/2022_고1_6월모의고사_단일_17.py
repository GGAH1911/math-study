from sympy import symbols, expand
x = symbols('x')
a, b = -5, 3
P = x**3 + x**2 + a*x + b
Q = x + 3
product = expand((x - 1)**2 * Q)
print('VERIFY_PASS' if product == P else 'VERIFY_FAIL')
ab = a * b
result = ab + 3
print(result)