from fractions import Fraction

# a_1 = 4로 순방향 확인
a = [None, Fraction(4)]  # a[0]은 미사용, a[1] = 4

# 규칙: n이 홀수면 a_{n+1} = 1/a_n, n이 짝수면 a_{n+1} = 8*a_n
for n in range(1, 12):
    if n % 2 == 1:  # n이 홀수
        a_next = 1 / a[n]
    else:  # n이 짝수
        a_next = 8 * a[n]
    a.append(a_next)

# a_12가 1/2인지 확인
if a[12] == Fraction(1, 2) and a[1] + a[4] == Fraction(9, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')