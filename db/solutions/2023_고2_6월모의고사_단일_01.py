import sympy as sp

# 문제의 해석: √((3^2 + √2)^2) - √2
sqrt2 = sp.sqrt(2)
result = sp.sqrt((9 + sqrt2)**2) - sqrt2
result_simplified = sp.simplify(result)

if result_simplified == 9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result_simplified}')