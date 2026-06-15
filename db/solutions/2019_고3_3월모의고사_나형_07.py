from sympy import *
a_values = []
for a in range(1, 11):
    result = a**(Rational(1,3))
    if result.is_integer:
        a_values.append(a)
total = sum(a_values)
if total == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')