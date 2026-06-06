from sympy import symbols, simplify
a, b, n = 1, 3, 12
lhs = (2**a * 4**b * 3**b)**n
rhs = 2**84 * 3**36
if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')