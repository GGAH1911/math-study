from itertools import product

# X = {1, 2, 3, 4}
X = [1, 2, 3, 4]

# 조건을 만족하는 함수 f의 개수 세기
count = 0
for f1 in X:  # f(1) 선택
    for f2 in X:  # f(2) 선택
        for f3 in X:  # f(3) 선택
            for f4 in X:  # f(4) 선택
                # 조건: f(2) <= f(3) <= f(4)
                if f2 <= f3 <= f4:
                    count += 1

if count == 80:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {count}')