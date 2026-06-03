from sympy import symbols, div, simplify
x = symbols('x')
P = x**2 - 2*x + 6
divisor = x + 1
quotient, remainder = div(P, divisor, domain='ZZ')
result = remainder
print('VERIFY_PASS' if result == 9 else 'VERIFY_FAIL')