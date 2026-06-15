import sympy as sp
x = sp.Symbol('x')
f = sp.sqrt(x + 1) + 1
g = (x - 1)**2 - 1
composition = g.subs(x, f)
composition_simplified = sp.simplify(composition)
result_15 = composition_simplified.subs(x, 15)
result_5 = composition_simplified.subs(x, 5)
print(f'(g∘f)(x) simplified: {composition_simplified}')
print(f'(g∘f)(15) = {result_15}')
print(f'(g∘f)(5) = {result_5}')
if result_5 == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')