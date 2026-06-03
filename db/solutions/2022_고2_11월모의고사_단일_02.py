from sympy import symbols
a1 = symbols('a1')
d = 3
a7 = a1 + 6*d
a2 = a1 + 1*d
result = a7 - a2
if result == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')