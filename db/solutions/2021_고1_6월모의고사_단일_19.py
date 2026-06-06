from sympy import I, sqrt, simplify, expand

z = -1/2 + sqrt(3)/2 * I
z_bar = -1/2 - sqrt(3)/2 * I

# 조건 검증
assert abs(expand(z + z_bar + 1)) < 1e-10, 'z + z_bar = -1 실패'
assert abs(expand(z * z_bar - 1)) < 1e-10, 'z*z_bar = 1 실패'

# 주어진 식 계산
S = (z_bar/z**5) + (z_bar**2/z**4) + (z_bar**3/z**3) + (z_bar**4/z**2) + (z_bar**5/z)
S_simplified = simplify(S)

if abs(S_simplified - 5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')