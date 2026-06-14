import sympy as sp
cos_val = -sp.sqrt(5)/5
sin_val = 2 * cos_val
tan_val = sin_val / cos_val

verify = (sin_val * cos_val) / (1 - cos_val) + (1 - cos_val) / tan_val
result = sp.simplify(verify)

if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')