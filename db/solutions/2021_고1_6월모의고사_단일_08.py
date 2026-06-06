import sympy as sp
x, a_val, b_val = sp.symbols('x a_val b_val')
a_val = -4
b_val = 1
f = x**3 + a_val*x**2 + b_val*x + 6
f_at_1 = f.subs(x, 1)
f_at_3 = f.subs(x, 3)
remainder_check = (f_at_1 == 4)
divisible_check = (f_at_3 == 0)
if remainder_check and divisible_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')