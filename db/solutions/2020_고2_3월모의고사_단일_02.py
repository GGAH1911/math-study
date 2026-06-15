import sympy as sp
i = sp.I
expr = 1 + i**2
result = sp.simplify(expr)
print('VERIFY_PASS' if result == 0 else f'VERIFY_FAIL: got {result}')