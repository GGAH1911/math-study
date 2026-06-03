import math

def check(x):
    # 진수 조건
    if x <= 0 or x - 6 <= 0:
        return False
    lhs = math.log2(x)
    rhs = 4 - math.log2(x - 6)
    return lhs <= rhs + 1e-9

# 정수 후보: 충분한 범위에서 탐색
candidates = [x for x in range(1, 100) if check(x)]
total = sum(candidates)

if candidates == [7, 8] and total == 15:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: candidates={candidates}, sum={total}')
