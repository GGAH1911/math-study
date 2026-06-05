import sympy as sp
a, b = 1, -5
expr = (4**a * 6) / (3**b)
n_cubed = sp.Rational(4**a * 6) * sp.Rational(3**(-b))
n = n_cubed ** sp.Rational(1, 3)
original_expr = sp.Rational(4**a * 6) * sp.Rational(3, 1)**(-b)
result = original_expr ** sp.Rational(1, 3)
is_natural = result == sp.Integer(18)
in_range = 10 <= int(result) <= 20
print('VERIFY_PASS' if is_natural and in_range else 'VERIFY_FAIL')