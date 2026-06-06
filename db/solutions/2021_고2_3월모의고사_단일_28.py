from itertools import combinations

# 조건 (가) 검증
A = {3, 4, 5}
B = {1, 2, 3, 5}
U = {1, 2, 3, 4, 5}

A_complement = U - A
B_complement = U - B

if A_complement | B_complement != {1, 2, 4}:
    print('VERIFY_FAIL')
else:
    # 조건 (나) 검증
    valid = True
    for x in U:
        X = {x}
        A_union_X = A | X
        result_set = A_union_X - B
        if len(result_set) != 1:
            valid = False
            break
    
    if valid:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')