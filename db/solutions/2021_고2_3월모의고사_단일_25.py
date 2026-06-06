import sympy as sp
x = sp.Symbol('x')
a, b = 2, 1
P = (x+2)*(x-1)*(x+a) + b*(x-1)
divisor = x**2 + 4*x + 5
quotient, remainder = sp.div(P, divisor)
if remainder == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')