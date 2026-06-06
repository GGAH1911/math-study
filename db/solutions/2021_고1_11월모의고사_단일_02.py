import sympy as sp
x = sp.symbols('x')
a_val, b_val = 2, 4
left = x**2 + (a_val + 1)*x + 4
right = x**2 + 3*x + b_val
diff = sp.expand(left - right)
if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')