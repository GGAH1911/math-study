import sympy as sp
a = 3 + sp.sqrt(10)
assert float(a) > 4
assert sp.simplify(a**2 - 6*a - 1) == 0
sin_a_2 = (a - 1) / (2 * a)
cos_a = 1 - 2 * sin_a_2**2
sin_g_2 = 4 / a
assert sp.simplify(cos_a - sin_g_2) == 0
result = sp.simplify(a**3 - 1/a**3)
assert result == 234
print('VERIFY_PASS')