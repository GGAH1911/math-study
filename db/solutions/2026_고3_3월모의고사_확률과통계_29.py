from itertools import permutations

white_numbers = [1, 3, 5, 7, 9]
black_numbers = [2, 4, 6, 8, 10]

count = 0

# 1을 고정하여 회전 제거
for perm in permutations([3, 5, 7, 9]):
    W = (1,) + perm
    
    for black_perm in permutations(black_numbers):
        B = black_perm
        
        # 원형 배열: W[0]-B[0]-W[1]-B[1]-W[2]-B[2]-W[3]-B[3]-W[4]-B[4]-(W[0])
        # 제약: 모든 이웃한 수의 곱이 70 이하
        constraints = [
            (W[0], B[0]), (B[0], W[1]), (W[1], B[1]), (B[1], W[2]),
            (W[2], B[2]), (B[2], W[3]), (W[3], B[3]), (B[3], W[4]),
            (W[4], B[4]), (B[4], W[0]),
        ]
        
        valid = True
        for a, b in constraints:
            if a * b > 70:
                valid = False
                break
        
        if valid:
            count += 1

if count == 864:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')