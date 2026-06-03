from sympy import symbols, expand, limit, simplify
x = symbols('x')
f = (x-3)*(x-4)*(x-6)
f_expanded = expand(f)
print(f'f(x) = {f_expanded}')
print(f'f(5) = {f.subs(x, 5)}')
print(f'f(8) = {f.subs(x, 8)}')
f_5_plus_1 = f.subs(x, 5) + 1
g_5 = (f.subs(x, 8) * f_5_plus_1) / f.subs(x, 5)
print(f'g(5) = {g_5}')
if g_5 == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')