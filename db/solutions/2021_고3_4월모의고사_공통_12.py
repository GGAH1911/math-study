import sympy as sp
x, a = sp.symbols('x a')
f = x**3 - 6*x**2 + 9*x + a
a_val = 8
f_evaluated = f.subs(a, a_val)
f_at_1 = f_evaluated.subs(x, 1)
f_at_0 = f_evaluated.subs(x, 0)
f_at_3 = f_evaluated.subs(x, 3)
max_val = max(float(f_at_0), float(f_at_1), float(f_at_3))
if max_val == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')