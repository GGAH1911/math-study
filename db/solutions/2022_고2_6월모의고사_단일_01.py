from sympy import root, simplify
val = root(3, 4) * root(27, 4)
result = simplify(val)
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')