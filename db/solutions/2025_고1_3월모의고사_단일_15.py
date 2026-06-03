from sympy import symbols, expand, factor
x = symbols('x')
f1 = x**2 + 12*x + 27
f2 = x**2 + 7*x - 18
fac1 = factor(f1)
fac2 = factor(f2)
common_factor = x + 9
if (x + 9) in fac1.as_ordered_factors() and (x + 9) in fac2.as_ordered_factors():
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')