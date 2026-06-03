import sympy as sp
x = sp.Symbol('x')
f = sp.tan(6*x) / (2*x)
limit_value = sp.limit(f, x, 0)
print(f'극한값: {limit_value}')
if limit_value == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')