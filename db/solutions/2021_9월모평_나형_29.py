from itertools import product

CANDIDATE = 168

# 흰 공 4개, 검은 공 6개를 세 상자 A, B, C에 분배
# 각 상자에 최소 2개씩

count = 0

# 모든 가능한 분배를 확인
for w_a in range(5):  # 흰 공 0~4개
    for w_b in range(5 - w_a):
        w_c = 4 - w_a - w_b
        if w_c < 0:
            continue
        
        for b_a in range(7):  # 검은 공 0~6개
            for b_b in range(7 - b_a):
                b_c = 6 - b_a - b_b
                if b_c < 0:
                    continue
                
                # 각 상자에 최소 2개씩 있는지 확인
                if (w_a + b_a >= 2 and 
                    w_b + b_b >= 2 and 
                    w_c + b_c >= 2):
                    count += 1

if count == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {CANDIDATE}, Got: {count}')