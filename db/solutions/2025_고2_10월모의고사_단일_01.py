import sympy as sp

expr = (3**(sp.sqrt(2)-1))**(sp.sqrt(2)+1)
result = sp.simplify(expr)
if result == 3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')