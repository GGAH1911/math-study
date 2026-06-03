import sympy as sp
x = sp.Symbol('x')
a_val, b_val = 5, 7
P = x**3 + a_val*x**2 + b_val*x + 3
quotient, remainder = sp.div(P, (x+1)**2)
if remainder == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')