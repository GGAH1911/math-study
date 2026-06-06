import sympy as sp
x = sp.Symbol('x')
# 원래 극한식
expr = (x - 3) / (sp.sqrt(x + 1) - 2)
limit_value = sp.limit(expr, x, 3)
print(f'극한값: {limit_value}')
if limit_value == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')