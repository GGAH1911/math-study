import math

# k의 값들에 따른 n 계산
valid_n_count = 0
for k in range(1, 41):
    if (4*k - 2) % 3 == 0:  # 지수가 정수 조건
        exp = (4*k - 2) // 3
        n = 2 ** exp
        # 원래 식에 역대입하여 검증
        log4_term = math.log(2 * n**2) / math.log(4)
        log2_term = 0.5 * math.log(math.sqrt(n)) / math.log(2)
        result = log4_term - log2_term
        # 결과가 자연수 k와 일치하는지 확인
        if abs(result - k) < 1e-9 and 1 <= k <= 40:
            valid_n_count += 1

if valid_n_count == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')