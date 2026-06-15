# 주어진 집합
A = {1, 3, 5}
B = {2, 3, 4}

# A - B 계산
diff = A - B
print(f'A - B = {diff}')

# 모든 원소의 합
sum_elements = sum(diff)
print(f'합 = {sum_elements}')

# 정답 확인
if sum_elements == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')