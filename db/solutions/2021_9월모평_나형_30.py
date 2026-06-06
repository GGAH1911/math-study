import sympy as sp
x, c = sp.symbols('x c', real=True)
f = c*(x-1)*(x-3)*(x+1)
f_at_0 = f.subs(x, 0)
f_at_8 = f.subs(x, 8)
f_at_minus6 = f.subs(x, -6)
h_at_8 = sp.Abs(f_at_8 * f_at_minus6)
result = h_at_8 / (f_at_0 * f_at_8)
result_simplified = sp.simplify(result)
print(f'f(0) = {f_at_0}')
print(f'f(8) = {f_at_8}')
print(f'f(-6) = {f_at_minus6}')
print(f'g(8) = {h_at_8}')
print(f'g(8)/(f(0)*f(8)) = {result_simplified}')
if result_simplified == 105:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')