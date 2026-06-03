import sympy as sp
x = sp.symbols('x')
a_val = 2
b_val = -3
lhs = x**2 + a_val*x - 3
rhs = x*(x+2) + b_val
if sp.expand(lhs - rhs) == 0:
    ans = a_val + b_val
    if ans == -1:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')