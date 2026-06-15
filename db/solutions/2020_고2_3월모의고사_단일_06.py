from sympy import symbols, div, Poly
x = symbols('x')
f = x**2 + 3*x + 6
divisor = x + 2
quotient, remainder = div(f, divisor, domain='ZZ')
print(f'Quotient: {quotient}, Remainder: {remainder}')
if remainder == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')