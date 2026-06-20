CANDIDATE = 58

# 일반항 공식 검증
def a_n(n):
    return (4*n - 3) / (4*n + 5)

# 원래 조건식 검증: sum_{k=1}^{n} (4k-3)/a_k = 2n^2 + 7n
def verify_sum_condition(n):
    total = sum((4*k - 3) / a_n(k) for k in range(1, n+1))
    expected = 2*n**2 + 7*n
    return abs(total - expected) < 1e-10

# 여러 n에 대해 검증
for n in [1, 2, 3, 5, 9]:
    if not verify_sum_condition(n):
        print('VERIFY_FAIL')
        exit()

# a_5, a_7, a_9 계산
a5 = a_n(5)
a7 = a_n(7)
a9 = a_n(9)

product = a5 * a7 * a9

# product = 17/41 확인
from fractions import Fraction
frac = Fraction(17, 41)
if abs(product - float(frac)) > 1e-10:
    print('VERIFY_FAIL')
    exit()

# p + q 계산
p = 41
q = 17
result = p + q

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')