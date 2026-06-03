from fractions import Fraction

# a_1 = 5/36
a1 = Fraction(5, 36)

# 수열 생성 (조건식 a_{n+1} = 1 - 4*S_n 이용)
a = [None, a1]  # a[1] = a_1
S = [None, a1]  # S[1] = a_1

for n in range(1, 6):
    a_next = 1 - 4 * S[n]
    a.append(a_next)
    S.append(S[n] + a_next)

# 조건 검증
assert a[4] == 4, f'a_4 = {a[4]}, expected 4'
assert a[1] * a[6] == 5, f'a_1 * a_6 = {a[1] * a[6]}, expected 5'

print('VERIFY_PASS')