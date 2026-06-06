from itertools import combinations_with_replacement

# 조건을 만족하는 모든 분배 확인
count_all = 0  # (가), (나) 만족
count_all_odd = 0  # (가), (나), 모두 홀수
count_at_least_one_even = 0  # (가), (나), (다) 만족

for a in range(1, 10):
    for b in range(1, 10):
        for c in range(1, 10):
            for d in range(1, 10):
                if a + b + c + d == 14:
                    count_all += 1
                    # 모두 홀수인지 확인
                    if a % 2 == 1 and b % 2 == 1 and c % 2 == 1 and d % 2 == 1:
                        count_all_odd += 1
                    # 적어도 하나가 짝수인지 확인
                    if not (a % 2 == 1 and b % 2 == 1 and c % 2 == 1 and d % 2 == 1):
                        count_at_least_one_even += 1

if count_at_least_one_even == 218 and count_all == 270 and count_all_odd == 52:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')