CANDIDATE = 18

def verify():
    count = 0
    # f(1)=1, f(2)=2, f(3)=3 고정
    fixed = {1:1, 2:2, 3:3}
    
    # 남은 값들의 모든 순열 확인
    from itertools import permutations
    for perm in permutations([4,5,6,7,8]):
        f = fixed.copy()
        f[4], f[5], f[6], f[7], f[8] = perm
        
        # 조건 (가) 확인: 소수 p에 대해 f(p)<=p
        if f[2] <= 2 and f[3] <= 3 and f[5] <= 5 and f[7] <= 7:
            # 조건 (나) 확인: 약수 관계 보존
            valid = True
            divisor_pairs = [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8),
                           (2,4), (2,6), (2,8), (3,6), (4,8)]
            for a, b in divisor_pairs:
                if f[a] >= f[b]:
                    valid = False
                    break
            if valid:
                count += 1
    
    if count == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: expected {CANDIDATE}, got {count}')

verify()