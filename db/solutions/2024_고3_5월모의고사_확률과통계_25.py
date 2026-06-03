from itertools import combinations_with_replacement

# 가능한 짝수들
evens = [4, 6, 8, 10, 12]

# 비내림차순 선택 (중복조합)
count = 0
for combo in combinations_with_replacement(evens, 4):
    x, y, z, w = combo
    if 4 <= x <= y <= z <= w <= 12:
        count += 1

if count == 70:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')