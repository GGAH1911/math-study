from sympy import symbols, simplify
x, a = symbols('x a')
f = x**3 - x**2 - 10*x + a
f_at_1 = f.subs(x, 1)
result = f_at_1.subs(a, 10)
if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')