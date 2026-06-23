from math import factorial, gcd

CANDIDATE = 12

# 전체 경우의 수
total = factorial(7)

# 흰 4와 검은 4가 이웃하는 경우
# (흰 4, 검은 4를 하나의 블록으로 취급 + 다른 5개 공)
neighbor_cases = factorial(6) * 2

# 같은 숫자가 이웃하지 않는 경우
valid_cases = total - neighbor_cases

# 확률 = 5/7
q = 5
p = 7

# 검증
if valid_cases == 3600 and total == 5040 and neighbor_cases == 1440:
    if gcd(q, p) == 1:
        if p + q == CANDIDATE:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')