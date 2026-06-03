import sympy as sp
a = sp.log(5, 3)
result = sp.simplify(3**a)
f_at_point = sp.simplify(3**(a+2-2) + a)
f_expected = a + 5
if result == 5 and sp.simplify(f_at_point - f_expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')