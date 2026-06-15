from sympy import symbols, limit, exp, oo
x = symbols('x')
f = (x**3 + 2*x) / (exp(3*x) - 1)
result = limit(f, x, 0)
expected = 2/3
if abs(float(result) - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')