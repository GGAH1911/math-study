import sympy as sp
val = sp.cbrt(-8) + sp.root(81, 4)
val = sp.nsimplify(sp.re(sp.N(sp.real_root(-8,3))) + sp.real_root(81,4))
cube = sp.real_root(-8, 3)
fourth = sp.real_root(81, 4)
result = sp.simplify(cube + fourth)
if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')