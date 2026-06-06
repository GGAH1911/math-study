import math

count = 0
for a in range(1, 20):
    for b in range(1, 100):
        # a^2 + b < 36
        if a*a + b >= 36:
            break
        
        # 근의 차를 직접 계산
        discriminant = 4*a*a + 4*b
        root_diff = 2 * math.sqrt(discriminant / 4)
        
        # 조건 확인
        if root_diff < 12:
            count += 1

if count == 120:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 120')