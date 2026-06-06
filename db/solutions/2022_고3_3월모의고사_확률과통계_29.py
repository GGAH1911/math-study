from math import comb

# 조건 (나) 불만족 함수 개수 검증
# 집합 정의
X = [1, 2, 3, 4, 5]
Y = [-1, 0, 1, 2, 3]

# 조건 (나) 불만족: -1과 1 동시 불포함 AND 0이 최대 1개
count = 0
for f1 in Y:
    for f2 in Y:
        for f3 in Y:
            for f4 in Y:
                for f5 in Y:
                    f = [f1, f2, f3, f4, f5]
                    # 조건 (가) 확인
                    if not all(f[i] <= f[i+1] for i in range(4)):
                        continue
                    # 조건 (나) 확인
                    found = False
                    for i in range(5):
                        for j in range(i+1, 5):
                            if f[i] + f[j] == 0:
                                found = True
                                break
                        if found:
                            break
                    if found:
                        count += 1

print(f"VERIFY_PASS" if count == 65 else f"VERIFY_FAIL: got {count}")