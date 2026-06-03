from sympy import symbols
a_val = 2
x = symbols('x')
f = x**3 - (a_val+1)*x**2 + (a_val-3)*x + 8
remainder = f.subs(x, a_val)
if remainder == a_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')