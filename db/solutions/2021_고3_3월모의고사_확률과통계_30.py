from itertools import product

# 조건 (가), (나)를 모두 만족하는 경우 직접 세기
count = 0
for seq in product(range(1, 5), repeat=4):
    # 조건 (가): 1이 최소 1회 이상
    if 1 not in seq:
        continue
    
    # 조건 (나): 이웃한 수의 차 ≤ 2
    valid = True
    for i in range(len(seq) - 1):
        if abs(seq[i] - seq[i+1]) > 2:
            valid = False
            break
    
    if valid:
        count += 1

if count == 97:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 97')