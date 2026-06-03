import sympy as sp
result = (3*sp.sqrt(3))**sp.Rational(1,3) * 3**sp.Rational(3,2)
result_simplified = sp.simplify(result)
print('VERIFY_PASS' if result_simplified == 9 else f'VERIFY_FAIL: got {result_simplified}')