import sympy as sp
x = sp.Symbol('x')
f = x**3 + x - 2
roots = sp.solve(f, x)
print(f'근들: {roots}')
alpha = roots[1]
beta = roots[2]
result = beta/alpha + alpha/beta
result_simplified = sp.simplify(result)
print(f'답: {result_simplified}')
expected = -3/2
if sp.simplify(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: 예상 {expected}, 계산 {result_simplified}')