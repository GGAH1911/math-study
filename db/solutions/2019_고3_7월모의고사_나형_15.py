from itertools import permutations

# 조건을 만족하는 k 찾기
for k_test in range(1, 20):
    # A = {2, 4, 9, d, e}라고 하면, d + e = 22
    # d, e는 {2+k, 4+k, 9+k}의 부분집합
    candidates = {2+k_test, 4+k_test, 9+k_test}
    
    # d + e = 22를 만족하는 쌍 찾기
    for d in candidates:
        e = 22 - d
        if e in candidates and d != e:
            # A 구성
            A = {2, 4, 9, d, e}
            
            # A가 5개 원소인지 확인
            if len(A) != 5:
                continue
            
            # B 구성
            B = {2+k_test, 4+k_test, 9+k_test, d+k_test, e+k_test}
            
            # 조건 확인
            if S_A := sum(A) == 37 and A - B == {2, 4, 9} and sum(A | B) == 92:
                print(f'VERIFY_PASS')