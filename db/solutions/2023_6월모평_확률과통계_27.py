from itertools import product, permutations

# 모든 가능한 배열을 직접 세기
characters = ['a', 'b', 'X', 'Y']
capitals = ['X', 'Y']
count = 0

# 6개 위치 모두를 순회
for arrangement in product(characters, repeat=6):
    # 조건 (가): 맨 앞과 맨 뒤가 대문자
    if arrangement[0] not in capitals or arrangement[5] not in capitals:
        continue
    
    # 조건 (나): 'a'가 정확히 한 번
    if arrangement.count('a') != 1:
        continue
    
    count += 1

if count == 432:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected 432, got {count}')