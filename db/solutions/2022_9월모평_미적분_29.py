import sympy as sp
a = sp.Symbol('a', real=True)
x = sp.Symbol('x', real=True)
f = -(x-a)**2 + 6
alpha = a - sp.sqrt(6)
beta = a + sp.sqrt(6)
f_alpha = f.subs(x, alpha)
f_beta = f.subs(x, beta)
print(f'f(alpha) = {sp.simplify(f_alpha)}')
print(f'f(beta) = {sp.simplify(f_beta)}')
if sp.simplify(f_alpha) == 0 and sp.simplify(f_beta) == 0:
    result = (alpha - beta)**2
    result = sp.simplify(result)
    print(f'(alpha - beta)^2 = {result}')
    if result == 24:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')