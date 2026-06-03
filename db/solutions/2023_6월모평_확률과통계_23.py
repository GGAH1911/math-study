import math
from math import factorial, comb

# 5개의 문자: a 3개, b 1개, c 1개
# 순열의 수 = 5! / (3! × 1! × 1!)
result = factorial(5) // (factorial(3) * factorial(1) * factorial(1))
print(result)

# 다른 방법: 조합으로 검증
# 5개 위치 중 a 배치: C(5,3)
# 남은 2개 중 b 배치: C(2,1)
# 남은 1개 중 c 배치: C(1,1)
alternative = comb(5, 3) * comb(2, 1) * comb(1, 1)
print(alternative)

if result == 20 and alternative == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')