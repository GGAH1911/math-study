import sympy as sp
x = sp.Symbol('x')
eq = (x**2 - 3*x) * (x**2 - 3*x + 6) + 5
roots = sp.solve(eq, x)
real_roots = [r for r in roots if r.is_real]
print(f'실근의 개수: {len(real_roots)}')
if len(real_roots) == 2:
    alpha, beta = real_roots[0], real_roots[1]
    product = alpha * beta
    product_simplified = sp.simplify(product)
    print(f'alpha = {alpha}')
    print(f'beta = {beta}')
    print(f'alpha * beta = {product_simplified}')
    if product_simplified == 1:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')