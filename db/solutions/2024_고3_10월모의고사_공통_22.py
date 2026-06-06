import sympy as sp
x = sp.Symbol('x')
f = (x + 3)**2 * x
f_expanded = sp.expand(f)
result = f.subs(x, 6)
verify_f_minus2 = f.subs(x, -2)
print(f'f(6) = {result}')
print(f'f(-2) = {verify_f_minus2}')
if verify_f_minus2 == -2 and result == 486:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')