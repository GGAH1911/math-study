from fractions import Fraction

a = 12
r = Fraction(1, 2)

# 조건 1: a_5 = 3/4
a5 = a * (r ** 4)
assert a5 == Fraction(3, 4), f'a5 check failed: {a5}'

# 조건 2: S_4 - S_2 = 3*a_4
S2 = a * (1 - r**2) / (1 - r) if r != 1 else None
S4 = a * (1 - r**4) / (1 - r) if r != 1 else None
a4 = a * (r ** 3)

assert S4 - S2 == 3 * a4, f'S_4 - S_2 check failed: {S4 - S2} != {3*a4}'

# 최종 답
a1 = a
a2 = a * r
result = a1 + a2
assert result == 18, f'Final result check failed: {result}'

print('VERIFY_PASS')