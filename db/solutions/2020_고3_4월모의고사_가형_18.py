from sympy import sqrt, Rational, simplify

# 계산 검증
k = Rational(16, 11)
r = Rational(8, 11)
r_squared = r**2

# 축소 비율 확인
B2C2 = 3 * k
B1C1 = 6
scale_ratio = B2C2 / B1C1
assert simplify(scale_ratio - r) == 0, f'Scale ratio mismatch: {scale_ratio} vs {r}'

# S1 계산
S1 = 6 * sqrt(2)

# 무한급수: S∞ = S1 / (1 - r²)
S_infinity = S1 / (1 - r_squared)
S_infinity_simplified = simplify(S_infinity)

# 정답 확인
expected = 242 * sqrt(2) / 19
if simplify(S_infinity_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')