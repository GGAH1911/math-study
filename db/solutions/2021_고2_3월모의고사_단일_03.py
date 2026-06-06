# A와 B 정의
A = {2, 3, 4, 5, 6}
a = 5
B = {1, 3, a}

# 교집합 계산
intersection = A & B

# 원소의 합 계산
sum_of_elements = sum(intersection)

# 검증
if sum_of_elements == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')