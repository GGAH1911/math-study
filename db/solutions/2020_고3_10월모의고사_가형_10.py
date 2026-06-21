from math import factorial
from itertools import permutations

# 각 경우의 카드 선택
case1 = ['B', 'B', 'C', 'C', 'C']  # A 제외
case2 = ['A', 'B', 'C', 'C', 'C']  # B 제외
case3 = ['A', 'B', 'B', 'C', 'C']  # C 제외

def count_valid_arrangements(cards):
    """두 번째 위치에 C가 고정된 배열의 수를 센다"""
    # C를 제거하고 남은 카드
    remaining = cards[:]
    remaining.remove('C')
    
    # 남은 4개 카드의 순열
    valid = set()
    for perm in permutations(remaining):
        # 두 번째 위치에 C를 삽입
        arrangement = (perm[0], 'C', perm[1], perm[2], perm[3])
        valid.add(arrangement)
    
    return len(valid)

total = count_valid_arrangements(case1) + count_valid_arrangements(case2) + count_valid_arrangements(case3)

if total == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')