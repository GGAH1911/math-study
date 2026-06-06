from itertools import permutations

# A를 위치 0에 고정, 나머지 5명(B=1, C=2, D=3, E=4, F=5)을 배치
count = 0
for perm in permutations([1, 2, 3, 4, 5]):
    arrangement = [0] + list(perm)  # 위치 0~5에 배치된 사람
    
    # A=0의 위치
    pos_A = 0
    # B=1의 위치
    pos_B = arrangement.index(1)
    # C=2의 위치
    pos_C = arrangement.index(2)
    
    # 조건 (가): A(위치 0)와 B가 이웃하는가?
    neighbors_of_0 = {5, 1}  # 원탁에서 위치 0의 이웃
    if pos_B not in neighbors_of_0:
        continue
    
    # 조건 (나): B와 C가 이웃하지 않는가?
    neighbors_of_B = {(pos_B - 1) % 6, (pos_B + 1) % 6}
    if pos_C in neighbors_of_B:
        continue
    
    count += 1

if count == 36:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 36')