from fractions import Fraction

A = -3
B = 5

# 내분점 계산: AB를 1:3으로 내분
m, n = 1, 3
P = (m * B + n * A) / (m + n)

# 검증: 거리 비가 1:3인지 확인
dist_AP = abs(P - A)
dist_PB = abs(B - P)

if dist_AP > 0 and dist_PB > 0:
    ratio = dist_AP / dist_PB
    expected_ratio = m / n
    if abs(ratio - expected_ratio) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')