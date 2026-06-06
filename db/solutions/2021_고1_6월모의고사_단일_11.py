import sympy as sp
m, a, b, x = sp.symbols('m a b x', real=True)
a_val, b_val = sp.Rational(1, 2), sp.Rational(1, 4)
eq = x**2 - 2*(m + a_val)*x + m**2 + m + b_val
discriminant = sp.discriminant(eq, x)
discriminant_simplified = sp.simplify(discriminant)
if discriminant_simplified == 0:
    result = 12 * (a_val + b_val)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')