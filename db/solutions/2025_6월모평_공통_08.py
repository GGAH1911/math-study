from fractions import Fraction
a = -512
r = Fraction(-1, 2)
# 검증: a_6 = 16
a6 = a * (r ** 5)
assert a6 == 16, f'a_6 = {a6}, expected 16'
# 검증: 2*a_8 - 3*a_7 = 32
a7 = a * (r ** 6)
a8 = a * (r ** 7)
result = 2 * a8 - 3 * a7
assert result == 32, f'2a_8 - 3a_7 = {result}, expected 32'
# 검증: a_1 * a_2 < 0
a1 = a
a2 = a * r
assert a1 * a2 < 0, f'a_1 * a_2 = {a1 * a2}, expected < 0'
# 최종 답: a_9 + a_11
a9 = a * (r ** 8)
a11 = a * (r ** 10)
answer = a9 + a11
assert answer == Fraction(-5, 2), f'a_9 + a_11 = {answer}, expected -5/2'
print('VERIFY_PASS')