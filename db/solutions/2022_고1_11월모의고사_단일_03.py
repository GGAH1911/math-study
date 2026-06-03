from sympy import I, simplify
z = 2 + I
z_bar = 2 - I
result = z + I * z_bar
expected = 3 + 3*I
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')