from itertools import product

# 조건을 만족하는 함수의 개수를 세기
count = 0

for f1 in range(1, 5):  # f(1) ∈ {1,2,3,4}
    for f2 in range(1, 5):  # f(2) ∈ {1,2,3,4}
        # 조건 (가): f(1) + f(2) = 4
        if f1 + f2 != 4:
            continue
        
        # f(3), f(4), f(5)의 모든 조합
        for f3 in range(1, 5):
            for f4 in range(1, 5):
                for f5 in range(1, 5):
                    # 함수 f 정의
                    f_values = [f1, f2, f3, f4, f5]
                    
                    # 조건 (나): 1이 치역에 포함되는가?
                    codomain = set(f_values)
                    if 1 in codomain:
                        count += 1

if count == 165:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')