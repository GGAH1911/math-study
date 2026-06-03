# 4000 이상이면서 홀수인 네 자리 수 개수 검증
# 직접 세기로 확인

count = 0
for a in [4, 5]:  # 천의 자리: 4 이상
    for b in [1, 2, 3, 4, 5]:  # 백의 자리
        for c in [1, 2, 3, 4, 5]:  # 십의 자리
            for d in [1, 3, 5]:  # 일의 자리: 홀수
                number = a * 1000 + b * 100 + c * 10 + d
                if number >= 4000 and number % 2 == 1:
                    count += 1

expected = 150
if count == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected {expected}')