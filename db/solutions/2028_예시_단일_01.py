import sympy as sp

# 원래 식: (3^(3/2) * sqrt(3))^(1/2)
expr = (sp.Rational(3)**sp.Rational(3, 2) * sp.sqrt(3))**sp.Rational(1, 2)
result = sp.simplify(expr)

if result == 3:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')