import sympy as sp
# 원래 문제: 2^√3 × 2^(2-√3)
sqrt3 = sp.sqrt(3)
result = 2**sqrt3 * 2**(2 - sqrt3)
result_simplified = sp.simplify(result)
print(f'Result: {result_simplified}')
assert result_simplified == 4, f'Expected 4, got {result_simplified}'
print('VERIFY_PASS')