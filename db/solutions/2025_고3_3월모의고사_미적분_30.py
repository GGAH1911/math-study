from sympy import Rational
from math import gcd

CANDIDATE = 25

# ============================================================
# 문제 조건 인코딩 및 CANDIDATE 검증
# ============================================================

# 검증된 풀이로부터: r = 2/3, a_1 = 81/4
r = Rational(2, 3)
a_1 = Rational(81, 4)

# 등비수열: a_n = a_1 * r^(n-1)
def a_n(n):
    return a_1 * (r ** (n - 1))

# ============================================================
# 조건 1: 극한 조건 검증
# ============================================================
# lim_{n→∞} (a_1*a_{n+1} + a_{2n}) / (a_{n+1} + a_n) = 81/10
#
# a_{n+1} = a_1 * r^n
# a_{2n} = a_1 * r^(2n-1)
#
# 분자: a_1 * a_{n+1} + a_{2n} = a_1^2*r^n + a_1*r^(2n-1)
#                                = a_1*r^(n-1) * (a_1*r + r^n)
# 분모: a_{n+1} + a_n = a_1*r^n + a_1*r^(n-1)
#                      = a_1*r^(n-1) * (r + 1)
#
# 비: (a_1*r + r^n) / (r + 1)
# n→∞일 때, r^n → 0 (∵ |r| < 1)
# ∴ lim = a_1*r / (r + 1) = 81/10

limit_computed = a_1 * r / (r + 1)
limit_expected = Rational(81, 10)

if limit_computed != limit_expected:
    print("VERIFY_FAIL")
    exit()

# ============================================================
# 조건 2: 조건 (나) 검증
# ============================================================
# 0 < a_k < 10인 정수 a_k의 개수가 정확히 3
# (f는 주기 2이고, 정수점에서 극값을 가짐)

integer_count = 0
for k in range(1, 200):
    ak = a_n(k)
    # a_k가 정수인지 확인 (분모가 1)
    if ak.denominator == 1:
        ak_int = int(ak.p)
        if 0 < ak_int < 10:
            integer_count += 1
    # a_k가 음수면 이후 값들은 모두 음수이므로 종료
    if ak <= 0:
        break

if integer_count != 3:
    print("VERIFY_FAIL")
    exit()

# ============================================================
# 조건 3: a_7 = q/p 계산 및 최종 답 검증
# ============================================================
# a_7을 계산하고, q/p 기약분수 형태에서 p + q 계산

a_7 = a_n(7)

# Rational의 분자, 분모
# a_7 = Rational(numerator, denominator)
# q/p = a_7 ⟹ q = a_7.p (분자), p = a_7.q (분모)
q = a_7.p
p = a_7.q

# p, q가 서로소인지 확인
if gcd(p, q) != 1:
    print("VERIFY_FAIL")
    exit()

# p + q = CANDIDATE인지 확인
if p + q != CANDIDATE:
    print("VERIFY_FAIL")
    exit()

print("VERIFY_PASS")