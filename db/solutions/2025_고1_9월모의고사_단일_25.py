from sympy import symbols, expand

x = symbols('x')
P = x**2 - 2*x + 3

verify1 = P.subs(x, 1)  # P(1) should be 2
verify2 = P.subs(x, 2)  # P(2) should be 3
verify3 = P.subs(x, 3)  # P(3) is the answer

if verify1 == 2 and verify2 == 3:
    answer = verify3
    if answer == 6:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')