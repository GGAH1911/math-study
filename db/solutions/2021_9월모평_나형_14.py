from itertools import combinations, permutations

# A, B를 포함하여 5명 선택
total_count = 0
students = list(range(8))  # 0=A, 1=B, 2~7=나머지

# A, B는 0, 1로 고정
for others in combinations(range(2, 8), 3):
    selected = [0, 1] + list(others)
    
    # 원탁에서 회전 동치를 무시하고 배치
    # A, B가 이웃하는 경우를 세기
    count_ab_adjacent = 0
    
    # 첫 번째 사람을 고정하고 나머지 4명 배치
    fixed = selected[0]
    remaining = [p for p in selected if p != fixed]
    
    for perm in permutations(remaining):
        arrangement = [fixed] + list(perm)
        # 원형이므로 인덱스를 순환적으로 확인
        for i in range(5):
            next_i = (i + 1) % 5
            if (arrangement[i] == 0 and arrangement[next_i] == 1) or \
               (arrangement[i] == 1 and arrangement[next_i] == 0):
                count_ab_adjacent += 1
                break
    
    total_count += count_ab_adjacent

if total_count == 240:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {total_count}')