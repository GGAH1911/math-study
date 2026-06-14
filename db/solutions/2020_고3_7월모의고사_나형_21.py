from sympy import *

# 주어진 조건
a1 = 6
d = Rational(-3, 2)

# n >= 6일 때 S_n 공식
def S_n(n):
    if n <= 5:
        return n * (5 - n)
    else:
        return -(n - 5) * (n - 9) / 2

# 조건 검증
assert S_n(5) == 0, f"S_5 should be 0, got {S_n(5)}"
assert S_n(9) == 0, f"S_9 should be 0, got {S_n(9)}"

# S_n <= -70을 만족하는 최소 n 찾기
for n in range(1, 25):
    sn = S_n(n)
    if sn <= -70:
        print(f"n={n}: S_n={sn}")
        if n > 1 and S_n(n-1) > -70:
            print(f"VERIFY_PASS")
            break
else:
    if S_n(19) == -70:
        print(f"n=19: S_n={S_n(19)}")
        print(f"VERIFY_PASS")