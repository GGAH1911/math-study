import math
from itertools import permutations

# 블록 배치: 5개 단위를 원탁에 배치 (회전 동치)
circular_arrangements = math.factorial(4)  # (5-1)!

# 1학년 2명 블록 내 순열
group1_perm = math.factorial(2)

# 2학년 2명 블록 내 순열
group2_perm = math.factorial(2)

# 전체 경우의 수
total = circular_arrangements * group1_perm * group2_perm

print(f'원탁 배치 (5개 단위): {circular_arrangements}')
print(f'1학년 블록 내 순열: {group1_perm}')
print(f'2학년 블록 내 순열: {group2_perm}')
print(f'전체 경우의 수: {total}')

if total == 96:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')