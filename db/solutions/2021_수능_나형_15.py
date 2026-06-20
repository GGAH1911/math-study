from itertools import permutations

count = 0

# A를 위치 0에 고정, 나머지 5명의 배치
for perm in permutations([1, 2, 3, 4, 5]):
    arrangement = [0] + list(perm)
    
    a_pos = 0
    b_pos = arrangement.index(1)
    c_pos = arrangement.index(2)
    
    # 조건 (가): A와 B가 이웃
    neighbors_a = {(a_pos - 1) % 6, (a_pos + 1) % 6}
    if b_pos not in neighbors_a:
        continue
    
    # 조건 (나): B와 C가 이웃하지 않음
    neighbors_b = {(b_pos - 1) % 6, (b_pos + 1) % 6}
    if c_pos in neighbors_b:
        continue
    
    count += 1

if count == 36:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')