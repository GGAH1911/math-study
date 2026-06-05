from itertools import permutations

count = 0
for perm in permutations(['A', 'B', 'C', 'D', 'E', 'F']):
    b_idx = perm.index('B')
    c_idx = perm.index('C')
    a_idx = perm.index('A')
    
    min_bc = min(b_idx, c_idx)
    max_bc = max(b_idx, c_idx)
    
    # B와 C 사이에 1개 이상의 문자 존재
    if max_bc - min_bc > 1:
        # B와 C 사이에 A가 존재
        if min_bc < a_idx < max_bc:
            count += 1

if count == 240:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 240')