import itertools

# 모든 순열 생성
card_count = 0
for perm in itertools.permutations([1, 2, 3, 4, 5, 6]):
    first = perm[0]
    last = perm[-1]
    product = first * last
    if product % 2 == 1:  # 곱이 홀수
        card_count += 1

if card_count == 144:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')