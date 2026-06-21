from itertools import combinations

# 1부터 10까지의 수를 mod 3으로 분류
mask = [1 % 3, 2 % 3, 3 % 3, 4 % 3, 5 % 3, 6 % 3, 7 % 3, 8 % 3, 9 % 3, 10 % 3]

# 조건을 만족하는 4원소 부분집합의 개수
valid_count = 0
total_count = 0

for subset in combinations(range(10), 4):
    total_count += 1
    # 이 부분집합의 세 원소 조합을 모두 확인
    is_valid = True
    for three_subset in combinations(subset, 3):
        sum_mod3 = sum(mask[i] for i in three_subset) % 3
        if sum_mod3 == 0:
            is_valid = False
            break
    if is_valid:
        valid_count += 1

probability = valid_count / total_count
target = 3 / 14

if abs(probability - target) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {probability} != {target}')