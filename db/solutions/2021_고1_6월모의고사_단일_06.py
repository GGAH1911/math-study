import sympy as sp
i = sp.I
x = (1 - i) / (1 + i)
y = (1 + i) / (1 - i)
result = sp.simplify(x + y)
if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')