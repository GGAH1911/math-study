from sympy import sqrt, symbols, simplify

# 문제 조건
a = sqrt(3)
b_squared = 27
b = sqrt(b_squared)

# 점근선 기울기 검증
asymptote_slope = b / a
print('점근선 기울기:', asymptote_slope)
assert simplify(asymptote_slope - 3) == 0, 'VERIFY_FAIL'

# 주축 길이
major_axis_length = 2 * a
print('주축 길이:', major_axis_length)
assert simplify(major_axis_length - 2*sqrt(3)) == 0, 'VERIFY_FAIL'

print('VERIFY_PASS')