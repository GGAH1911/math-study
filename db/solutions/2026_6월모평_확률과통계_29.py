from math import gcd

# 전체 경우의 수
total = 6**3  # 216

# 조건을 만족하는 경우의 수 계산
count = 0
for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            if (a + b == 8) or (b >= c):
                count += 1

# 확률
prob_num = count
prob_den = total

# 기약분수로 변환
g = gcd(prob_num, prob_den)
q = prob_num // g
p = prob_den // g

# 검증
if q == 17 and p == 27 and gcd(p, q) == 1:
    result = p + q
    if result == 44:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')