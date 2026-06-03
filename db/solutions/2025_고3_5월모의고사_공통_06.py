import sympy as sp

cos_t = sp.Rational(1, 3)
sin_t = -sp.sqrt(1 - cos_t**2)  # 4사분면: sin < 0
tan_t = sin_t / cos_t

# 원래 조건 검증: sin*tan + cos == 3
lhs = sin_t * tan_t + cos_t
assert lhs == 3, f'조건 불만족: {lhs}'

# 구하는 값
result = sin_t - tan_t
expected = sp.Rational(4,3) * sp.sqrt(2)

if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: result={result}, expected={expected}')
