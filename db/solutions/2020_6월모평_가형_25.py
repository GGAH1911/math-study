from itertools import combinations

CANDIDATE = 60

X = {1, 2, 3, 4, 5}
count = 0

# 고정점 3개를 선택
for fixed_points in combinations(X, 3):
    F = set(fixed_points)
    N = X - F
    b, c = sorted(N)
    
    # Case 1: f(b) = c, f(c) ∈ F
    for fc in F:
        f = {}
        for x in F:
            f[x] = x
        f[b] = c
        f[c] = fc
        
        # 조건 확인
        fixed_count = sum(1 for x in X if f[x] == x)
        image = set(f[x] for x in X)
        image_size = len(image)
        
        if fixed_count == 3 and image_size == 4:
            count += 1
    
    # Case 2: f(b) ∈ F, f(c) = b
    for fb in F:
        f = {}
        for x in F:
            f[x] = x
        f[b] = fb
        f[c] = b
        
        # 조건 확인
        fixed_count = sum(1 for x in X if f[x] == x)
        image = set(f[x] for x in X)
        image_size = len(image)
        
        if fixed_count == 3 and image_size == 4:
            count += 1

if count == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {CANDIDATE}, got {count}')