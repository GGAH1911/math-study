from sympy import I, simplify, expand
z1 = 4 + I
z2 = 1 - 2*I
result = z1 + z2
answer = 5 - I
if simplify(result - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')