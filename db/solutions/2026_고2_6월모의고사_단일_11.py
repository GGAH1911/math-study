import math

# 자연수 k 범위: 2, 3, 4
k_values = [2, 3, 4]
valid_k = []

for k in k_values:
    # AB 거리 계산
    # 점 A: (k, 2*log_2(k))
    # 점 B: (k, -log_2(k))
    AB = 3 * math.log2(k)
    
    # 조건 확인: 3 <= AB <= 6
    if 3 <= AB <= 6:
        valid_k.append(k)
        print(f'k={k}: AB={AB:.4f} (valid)')
    else:
        print(f'k={k}: AB={AB:.4f} (invalid)')

# 합 계산
total = sum(valid_k)
print(f'\nValid k values: {valid_k}')
print(f'Sum: {total}')

if total == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')