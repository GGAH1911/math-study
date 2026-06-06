import sympy as sp
result = sp.Rational(1, 3) + sp.Rational(2, 3)
exponent_sum = result
final_value = 2 ** exponent_sum
if final_value == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')