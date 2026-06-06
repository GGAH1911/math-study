from itertools import combinations, permutations

X = {1, 2, 3, 4, 5, 6}
count = 0

# 조건 (가) 만족: f(1) > f(2) > f(3) > f(4)
# 조건 (나): 역함수 존재 안 함 = 전단사 아님

# 조건 (가)를 만족하는 모든 함수 생성
for f1, f2, f3, f4 in combinations(X, 4):
    # 내림차순으로 정렬
    vals_sorted = sorted([f1, f2, f3, f4], reverse=True)
    f1_val, f2_val, f3_val, f4_val = vals_sorted
    
    # f(5), f(6)은 X의 임의의 원소
    for f5 in X:
        for f6 in X:
            f_dict = {1: f1_val, 2: f2_val, 3: f3_val, 4: f4_val, 5: f5, 6: f6}
            
            # 조건 (가) 확인
            cond_a = True
            for x1 in range(1, 5):
                for x2 in range(x1 + 1, 5):
                    if not (f_dict[x1] > f_dict[x2]):
                        cond_a = False
                        break
            
            if not cond_a:
                continue
            
            # 조건 (나) 확인: 역함수 존재하지 않음 = 전단사 아님
            is_bijection = len(set(f_dict.values())) == 6
            
            if not is_bijection:
                count += 1

if count == 510:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 510')