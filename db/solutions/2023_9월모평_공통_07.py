from fractions import Fraction

# 원래 조건: S_n = 1/(n(n+1))
def S(n):
    return Fraction(1, n*(n+1))

# a_n 계산
def a(n):
    if n == 1:
        return S(1)
    else:
        return S(n) - S(n-1)

# 합 계산
total = Fraction(0)
for k in range(1, 11):
    total += S(k) - a(k)

if total == Fraction(9, 10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')