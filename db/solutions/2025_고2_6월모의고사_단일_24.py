import math

# 주어진 조건: log_2(x-1) < 5를 만족하는 자연수 x의 개수
answer = 31

# 검증: 답이 31이라면, 자연수 x는 2부터 32까지여야 함
count = 0
for x in range(1, 100):
    if x > 0:  # 자연수
        if x - 1 > 0:  # 로그 정의역
            log_val = math.log2(x - 1)
            if log_val < 5:
                count += 1

if count == answer:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {answer}, got {count}')