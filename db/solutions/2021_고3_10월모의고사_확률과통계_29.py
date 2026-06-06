from itertools import product

# 6자리 수: 각 자리에 1, 2, 3 배치
# 조건: 1, 2, 3 모두 최소 한 번 나타남
# 조건: 일의 자리(idx 0)와 백의 자리(idx 2)가 같음

count = 0
for digits in product([1, 2, 3], repeat=6):
    # 일의 자리: digits[0], 백의 자리: digits[2]
    if digits[0] != digits[2]:
        continue
    
    # 1, 2, 3이 모두 나타나는가?
    if set(digits) != {1, 2, 3}:
        continue
    
    count += 1

if count == 150:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 150')