from sympy import symbols, exp, limit
x = symbols('x')
f = (exp(6*x) - exp(4*x)) / (2*x)
limit_value = limit(f, x, 0)
if limit_value == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')