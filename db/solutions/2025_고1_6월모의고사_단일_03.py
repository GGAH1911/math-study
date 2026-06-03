import sympy as sp
x = sp.Symbol('x')
inequality = x**2 - 5*x + 4 < 0
roots = sp.solve(x**2 - 5*x + 4, x)
print(f'근: {sorted(roots)}')
if sorted(roots) == [1, 4]:
    a = 4
    test_val = 2.5
    result = test_val**2 - 5*test_val + 4
    if result < 0 and 1 < test_val < a:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')