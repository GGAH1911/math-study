import sympy as sp
x = sp.Symbol('x')
numerator = sp.ln(1 + 3*x)
denominator = sp.ln(1 + 5*x)
limit_value = sp.limit(numerator / denominator, x, 0)
answer = sp.Rational(3, 5)
if limit_value == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')