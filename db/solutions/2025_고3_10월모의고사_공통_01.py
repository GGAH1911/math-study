import sympy as sp
base = sp.Rational(3)
term1 = base**(sp.Rational(1,3))
term2 = sp.Integer(9)**(sp.Rational(1,3))
result = term1 * term2
simplified = sp.simplify(result)
if simplified == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')