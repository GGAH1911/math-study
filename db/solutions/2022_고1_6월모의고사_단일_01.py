from sympy import I, simplify
result = 1 + 2*I + I*(1 - I)
result_simplified = simplify(result)
answer = 2 + 3*I
if result_simplified == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')