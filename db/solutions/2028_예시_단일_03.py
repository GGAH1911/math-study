# 1~5 중에서 중복을 허용하여 4개를 택해 네 자리 수를 만들 때 짝수의 개수
# 짝수 조건: 일의 자리가 2 또는 4

count = 0
for d1 in range(1, 6):  # 천의 자리
    for d2 in range(1, 6):  # 백의 자리
        for d3 in range(1, 6):  # 십의 자리
            for d4 in [2, 4]:  # 일의 자리 (짝수만)
                number = d1 * 1000 + d2 * 100 + d3 * 10 + d4
                if number % 2 == 0:  # 짝수 검증
                    count += 1

if count == 250:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')