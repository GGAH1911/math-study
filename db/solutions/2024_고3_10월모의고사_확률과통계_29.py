# 모든 함수 f: X → Y에 대해 조건 검증
count = 0
X = [1, 2, 3, 4]
Y = [0, 1, 2, 3, 4, 5]

# 모든 가능한 함수 f를 생성 (f(1), f(2), f(3), f(4))의 모든 조합)
for f1 in Y:
    for f2 in Y:
        for f3 in Y:
            for f4 in Y:
                f = {1: f1, 2: f2, 3: f3, 4: f4}
                
                # 조건 (가): f(1) <= f(2) <= f(3) <= f(4)
                condition_ga = (f[1] <= f[2] <= f[3] <= f[4])
                
                # 조건 (나): f(a) = a를 만족하는 a의 개수가 정확히 1
                fixed_points = sum(1 for a in X if f[a] == a)
                condition_na = (fixed_points == 1)
                
                if condition_ga and condition_na:
                    count += 1

if count == 48:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')