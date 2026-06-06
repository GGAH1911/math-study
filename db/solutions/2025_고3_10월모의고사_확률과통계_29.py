from itertools import combinations, product

X = {2, 3, 5, 7, 11}
count = 0

# (b1, b2) 선택
for b1, b2 in combinations([3, 5, 7, 11], 2):
    A = {2, b1, b2}
    B = {b1, b2}
    A_list = sorted(A)
    B_list = sorted(B)
    
    # 조건 검증
    prod_A = 1
    for a in A_list:
        prod_A *= a
    prod_B = 1
    for b in B_list:
        prod_B *= b
    
    if prod_A != 2 * prod_B:
        continue
    
    X_minus_A = sorted(X - A)
    
    # f|_A: A -> {b1, b2} 전사함수
    for f_A_vals in product([b1, b2], repeat=3):
        f_A = dict(zip(A_list, f_A_vals))
        if len(set(f_A_vals)) != 2:
            continue
        
        # f|_{X\\A}: X\\A -> A, 2 포함
        for f_rest in product(A_list, repeat=2):
            f_rest_dict = dict(zip(X_minus_A, f_rest))
            
            # 2가 포함되는지 확인
            if 2 not in set(f_rest):
                continue
            
            # f 전체 정의
            f = {**f_A, **f_rest_dict}
            
            # f(X) = A 확인
            f_X = set(f.values())
            if f_X != A:
                continue
            
            # f(A) = B 확인
            f_A_comp = {f[a] for a in A}
            if f_A_comp != B:
                continue
            
            count += 1

if count == 180:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')